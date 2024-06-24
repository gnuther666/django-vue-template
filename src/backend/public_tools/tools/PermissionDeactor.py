from functools import wraps
from .response import CommonResponse
def get_permission_list(user)->set:
    return user.user_permissions()

def check_permission(user, need_permission):
    has_permission = get_permission_list(user)
    need_permission_str_list = set([one.name for one in need_permission])
    return need_permission_str_list.issubset(has_permission)


def use_permission(permissions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_obj = args[1].user
            if not check_permission(user_obj, permissions):
                return CommonResponse(data={'msg': '没有权限'}, code=201)
            result = func(*args, **kwargs)
            print("After function")
            return result

        return wrapper

    return decorator