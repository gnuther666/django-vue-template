from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.views import TokenObtainPairView
from util.response import CommonResponse
from app.models.app_user import AppUserModel
from util.redis_cache import RedisCache
from public_tools.tools.read_env import GetEnv
import logging

captcha_method = GetEnv().get_env().captcha
logger = logging.getLogger('django')

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):

        username = request.data.get('username')
        password = request.data.get('password')
        
        logger.debug(f'用户登录信息:username={username}, password={password}')
        if captcha_method in ['base', ]:
            check_success, error_msg = self.__verify_captcha(request)
            if not check_success:
                return CommonResponse(data={'msg': f'验证码错误:{error_msg}'}, code=201)
        user = None

        user = AppUserModel.objects.filter(username=username).first()
        if not user:
            return CommonResponse(data={'msg': '用户不存在:{}'.format(username)}, code=201)
            # 判断密码是否正确
        if not check_password(password, user.password):
            return CommonResponse(data={'msg': '密码错误'}, code=201)
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        modified_response = {
            'access_token': access,
            'refresh_token': str(refresh),
            'username': user.username
        }
        return CommonResponse(data={'data': modified_response}, code=201)
    
    def __verify_captcha(self, request):
        verify_key = request.data.get('verify_key')
        verify_input = request.data.get('verify_input')
        logger.debug(f'用户验证信息:verify_key={verify_key}, verify_input={verify_input}')
        verify_result = RedisCache.verify_captcha_from_redis(verify_key, verify_input)
        if verify_result.is_success == False:
            return False, verify_result.msg
        return True, 'success'