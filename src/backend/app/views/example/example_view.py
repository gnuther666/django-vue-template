import logging, os
from app.views.example.example_serializer import ExampleSerializer
from app.models.app_user import AppUserModel
from rest_framework import viewsets
from rest_framework.decorators import action
from util.response import CommonResponse
from rest_framework.permissions import AllowAny
from util.read_env import GetEnv
from django.conf import settings


logger = logging.getLogger('django')

class ExampleViewset(viewsets.ModelViewSet):
    queryset = AppUserModel.objects.all()
    serializer_class = ExampleSerializer
    permission_classes = (AllowAny,)  # 如果允许匿名用户访问则修改这里
    
    @action(methods=['GET'], detail=False)
    def get_image_list(self, request, *args, **kwargs):
        base_dir = GetEnv().get_env().media_path
        example_dir = 'example_resource'
        example_image_path = os.path.join(base_dir, example_dir)
        files = os.listdir(example_image_path)
        file_urls = [f'/{settings.MEDIA_URL}/{example_dir}/{one}'.replace('//', '/') for one in files]
        resp = CommonResponse(data={'msg': '授权成功', 'data': {'images': file_urls}}, code=200)
        return resp
