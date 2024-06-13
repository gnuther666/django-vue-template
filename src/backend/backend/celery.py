from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
from django.conf import settings
from public_tools.tools.read_env import GetEnv

custom_config = GetEnv().get_env()

# 指定Django默认配置文件模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
# 为我们的项目myproject创建一个Celery实例。这里不指定broker backend 容易出现错误。
## celery start
broker_url = 'redis://:{auth}@{host}:{port}/{db}'.format(auth=custom_config.redis_password,
                                                         host=custom_config.redis_ip,
                                                         port=custom_config.redis_port,
                                                         db=3
                                                         )

# 设置存储结果的后台  结果队列的链接地址
result_backend = 'redis://:{auth}@{host}:{port}/{db}'.format(auth=custom_config.redis_password,
                                                             host=custom_config.redis_ip,
                                                             port=custom_config.redis_port,
                                                             db=4)
print('broker_url', broker_url)
print('result_backend', result_backend)

app = Celery('backend', broker=broker_url, backend=result_backend)

# 这里指定从django的settings.py里读取celery配置
app.config_from_object('django.conf:settings')
app.conf.beat_schedule_filename = custom_config.media_path + '/celerybeat-schedule.dat'
# 下面的设置就是关于调度器beat的设置,
# 具体参考https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
app.conf.beat_schedule = {
    'auto_check': {  # 取个名字
        'task': 'app.tasks.run_status_check',  # 设置是要将哪个任务进行定时
        'schedule': timedelta(seconds=10)  # 调用crontab进行具体时间的定义
    }
}
# 自动从所有已注册的django app中加载任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)