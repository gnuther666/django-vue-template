import logging, os
import uuid

from .sys_menu_serializer import FrontMenuSerializer
from app.models import FrontMenuModel
from rest_framework import viewsets
from rest_framework.decorators import action
from util.response import CommonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated


logger = logging.getLogger('app')

class SysMenuViewset(viewsets.ModelViewSet):
    queryset = FrontMenuModel.objects.all()
    serializer_class = FrontMenuSerializer
    permission_classes = (AllowAny,)  # 如果允许匿名用户访问则修改这里

    def list(self, request, *args, **kwargs):
        return self.queryset.all()

    def create(self, request, *args, **kwargs):
        datas = request.data
        datas['item_key'] = uuid.uuid4().hex[0:24]
        serializer = FrontMenuSerializer(data=datas)
        serializer.is_valid(raise_exception=True)
        FrontMenuModel.objects.create(**serializer.validated_data)
        return CommonResponse(data={'msg': 'create success'}, code=200)
    
    # @action(methods=['GET'], detail=False)
    # def get_image_list(self, request, *args, **kwargs):
    #     base_dir = GetEnv().get_env().media_path
    #     example_dir = 'example_resource'
    #     example_image_path = os.path.join(base_dir, example_dir)
    #     files = os.listdir(example_image_path)
    #     file_urls = [f'/{settings.MEDIA_URL}/{example_dir}/{one}'.replace('//', '/') for one in files]
    #     resp = CommonResponse(data={'msg': '授权成功', 'data': {'images': file_urls}}, code=200)
    #     return resp

