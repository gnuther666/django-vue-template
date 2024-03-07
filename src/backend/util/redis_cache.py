from django.core.cache import cache
import functools
import pickle
from util.sys_struct import BoolMsgResult


def redis_cache(key):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = cache.get(key)
            if result is not None:
                print('通过缓存')
                return pickle.loads(result)
            else:
                print('通过计算')
                result = func(*args, **kwargs)
                cache.set(key, pickle.dumps(result), timeout=60 * 5)
                return result
        return wrapper
    return decorator


def get_from_redis_or_func(key, func, args:list = list(), kwargs:dict=dict(), timeout=60 * 5):
    result = cache.get(key)
    if result is not None:
        return pickle.loads(result)
    else:
        result = func(*args, **kwargs)
        cache.set(key, pickle.dumps(result), timeout=timeout)
        return result

def set_cache(key, value, timeout=60):
    rst = cache.set(key, pickle.dumps(value), timeout=timeout)
    return rst

def get_cache(key):
    rst = cache.get(key)
    return pickle.loads(rst)

class RedisCache:

    @staticmethod
    def set_captcha_to_redis(key, value):
        set_cache(key, value, timeout=60 * 5)

    @staticmethod
    def verify_captcha_from_redis(key, value) -> BoolMsgResult:
        result = get_cache(key)
        if result is None:
            return BoolMsgResult(is_success=False, msg='缓存中没有该验证码')
        if result != value:
            return BoolMsgResult(is_success=False, msg=f'验证码错误input={value}, cache={result}')
        return BoolMsgResult(is_success=True, msg='验证码正确')
