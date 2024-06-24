from django.apps import AppConfig
from dataclasses import dataclass
import logging, os
from typing import List
from django.conf import settings
from importlib import import_module
from enum import Enum
logger = logging.getLogger('django')

@dataclass(frozen=True)
class PermissionType:
    PermissionKey: str
    PermissionName: str
    PermissionApp: str

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    __PERMISSION__ = None

    @staticmethod
    def get_all_permissions() -> List[PermissionType]:
        if AppConfig.__PERMISSION__ is not None:
            return AppConfig.__PERMISSION__
        AppConfig.__PERMISSION__ = list()
        apps = [one for one in settings.INSTALLED_APPS]
        for app in apps:
            app_path = import_module(app).__path__[0]
            permission_file = os.path.join(app_path, 'Permissions.py')
            if not os.path.isfile(permission_file):
                continue
            logger.debug('read_load:%s' % permission_file)
            module_name = f'{app}.Permissions'
            permission_module = import_module(module_name)
            if not hasattr(permission_module, 'PERMISSIONS'):
                continue
            app_permissions = getattr(permission_module, 'PERMISSIONS')
            if not isinstance(app_permissions, Enum):
                for one_permission in app_permissions:
                    one_perm_format = PermissionType(one_permission.name, one_permission.value, app)
                    AppConfig.__PERMISSION__.append(one_perm_format)
        return AppConfig.__PERMISSION__
