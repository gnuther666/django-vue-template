from django.contrib.auth.models import AbstractUser
from django.db import models
from public_tools.tools.read_env import GetEnv
from django.contrib.auth.hashers import make_password, check_password
import uuid


class AppUserModel(AbstractUser):
    id = models.CharField(primary_key=True, max_length=64, null=False)
    phone = models.CharField(max_length=18, null=False)

    class Meta:
        db_table = 'user'
        ordering = ['-username']
        verbose_name = '用户表'

    @staticmethod
    def gen_default_super_user():
        admin_user_name = GetEnv().get_env().super_user_name
        obj = AppUserModel.objects.filter(username=admin_user_name).first()
        if not obj:
            obj = AppUserModel()
            obj.id = uuid.uuid4().hex
        ori_password = GetEnv().get_env().super_user_password
        obj.password = make_password(ori_password)
        obj.is_superuser = True
        obj.username = GetEnv().get_env().super_user_name
        obj.email = 'default_super_user@example.com'
        obj.is_staff = True
        obj.is_active = True
        obj.phone = '18812345678'
        obj.save()
        print('生成默认超级用户成功')

    @staticmethod
    def check_password(username, password):
        obj = AppUserModel.objects.filter(username=username).first()
        if obj is None:
            return False
        return check_password(password, obj.password)

    


    