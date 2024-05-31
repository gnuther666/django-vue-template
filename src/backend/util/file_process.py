import hashlib
import os, logging
import shutil
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple

from django.conf import settings
from django.http import HttpResponse
from util.response import CommonResponse

logger = logging.getLogger('django')

@dataclass
class FileStruct(object):
    file_name: str
    file_path: str
    file_md5: str
    file_size: int

    def __str__(self):
        return f"file_name={self.file_name}, file_path={self.file_path}, file_md5={self.file_md5}, file_size={self.file_size}"

class UserFileProcess:
    @staticmethod
    def download_file(file_path, file_name):
        # 获取文件路径或从数据库中获取文件内容等
        file_path = file_path

        response = HttpResponse(open(file_path, 'rb').read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        response['Content-Disposition'] =  file_name
        return response

    @staticmethod
    def download_file_with_stream(stream, file_name):
        # 获取文件路径或从数据库中获取文件内容等
        response = HttpResponse(stream, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        response['Content-Disposition'] =  file_name
        return response


    def handle_upload_file_with_type(f, ori_file_name, type_name):
        file_extension = ori_file_name.split(".")[-1]
        file_uuid = uuid.uuid4().hex
        file_name = '{typename}_{date_str}_{random}.{extension}'.format(typename=type_name,
                                                                        date_str=datetime.now().strftime('%Y%m%d'),
                                                                        random=file_uuid, extension=file_extension)
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
        full_file_name = os.path.join(settings.MEDIA_ROOT, file_name)
        with open(full_file_name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return True, full_file_name, file_uuid

    @staticmethod
    def get_md5_and_size(file_name):
        with open(file_name, "rb") as f:
            md5 = hashlib.md5()
            total_bytes_read = 0
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
                total_bytes_read += len(chunk)

            file_size = total_bytes_read
            checked = md5.hexdigest()
        return checked, file_size


    @staticmethod
    def handle_upload_file_return_full_info(f, ori_file_name, type_name) -> Tuple[bool,FileStruct]:
        res = UserFileProcess.handle_upload_file_with_type(f, ori_file_name, type_name)
        if res[0] != True:
            raise RuntimeError(f'文件:{ori_file_name}上传失败')
        md5, file_size = UserFileProcess.get_md5_and_size(res[1])
        return True, FileStruct(os.path.basename(res[1]), res[1], md5, file_size)


    @staticmethod
    def copy_local_file_to_media(ori_file_path, type_name='common'):
        file_extension = ori_file_path.split(".")[-1]
        file_uuid = uuid.uuid4().hex
        file_name = '{typename}_{date_str}_{random}.{extension}'.format(typename=type_name,
                                                                        date_str=datetime.now().strftime('%Y%m%d'),
                                                                        random=file_uuid, extension=file_extension)
        full_file_name = os.path.join(settings.MEDIA_ROOT, file_name)
        shutil.copyfile(ori_file_path, full_file_name)
        return full_file_name

    @staticmethod
    def get_download_response(file_path):
        new_path = UserFileProcess.convert_local_path_to_media_path(file_path)
        data={'file_path': new_path}
        return CommonResponse(data={'data': data}, code=200)
    
    @staticmethod
    def convert_local_path_to_media_path(local_path):
        logger.debug(f'查看路由转换后的路径：原{local_path}, 替{settings.MEDIA_ROOT}, 为{settings.MEDIA_URL}')
        replaced_path = local_path.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)
        if replaced_path.find(settings.MEDIA_ROOT) == -1:
            replaced_path = os.path.join(settings.MEDIA_URL, replaced_path)
        return replaced_path
