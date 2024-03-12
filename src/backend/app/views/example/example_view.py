import logging, os
from app.views.example.example_serializer import ExampleSerializer
from app.models.app_user import AppUserModel
from rest_framework import viewsets
from rest_framework.decorators import action
from util.response import CommonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from util.read_env import GetEnv
from django.conf import settings
from util.file_process import UserFileProcess, FileStruct


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
    
    @action(methods=['GET'], detail=False)
    def get_example_file(self, request, *args, **kwargs):
        file='example_resource/1.png'
        return UserFileProcess.get_download_response(file)


class ExampleLoginedViewset(viewsets.ModelViewSet):
    queryset = AppUserModel.objects.all()
    serializer_class = ExampleSerializer
    permission_classes = (IsAuthenticated, )

    @action(methods=['POST'], detail=False)
    def post_file_upload(self, request, *args, **kwargs):
        file = request.FILES['file']
        ori_file_name = file.name.lower()
        is_success, file_struct = UserFileProcess.handle_upload_file_return_full_info(file, ori_file_name, 'settle')
        if not is_success:
            return CommonResponse(data={'data': '文件上传失败', 'msg': '文件上传失败'}, code=201)
        return CommonResponse(data={'data': '文件上传成功', 'msg': f'文件上传成功{str(file_struct)}'}, code=200)
