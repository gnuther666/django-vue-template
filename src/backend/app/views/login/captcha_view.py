from util.captcha import Captcha
from util.response import CommonResponse
from util.redis_cache import RedisCache
from util.read_env import GetEnv


def get_captcha(request):
    captcha_method = GetEnv().get_env().captcha
    if captcha_method not in ['base', ]:
        return CommonResponse(data={'data': None, 'msg': '当前配置未开启验证码获取'}, code=201)
    obj = Captcha()
    rst = obj.get_captcha()
    RedisCache.set_captcha_to_redis(rst['key'], rst['captcha_text'])
    data = {'image_hex': rst['out_buff'], 'key': rst['key']}
    return CommonResponse(data={'data': data}, code=200)
