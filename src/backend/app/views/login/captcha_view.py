from util.captcha import Captcha
from util.response import CommonResponse
from util.redis_cache import RedisCache


def get_captcha(request):
    obj = Captcha()
    rst = obj.get_captcha()
    RedisCache.set_captcha_to_redis(rst['key'], rst['captcha_text'])
    data = {'image_hex': rst['out_buff'], 'key': rst['key']}
    return CommonResponse(data={'data': data}, code=200)
