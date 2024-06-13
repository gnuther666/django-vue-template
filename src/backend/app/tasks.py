import logging
from backend.celery import app
import datetime
from django.core.cache import caches

logger = logging.getLogger('celery')

@app.task
def run_status_check():
    cache = caches['default']
    last_time = cache.get('LAST_CHECK_TIME')
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cache.set('LAST_CHECK_TIME', current_time, 30)
    logger.info(f'django run status check: last time: {last_time}')
    return None