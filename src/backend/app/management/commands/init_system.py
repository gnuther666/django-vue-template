from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from app.models import AuthGroupExpander, AppUserModel
from app.apps import AppConfig
from django.contrib.auth.models import Group
import logging

logger = logging.getLogger('app')
class Command(BaseCommand):
    help = 'init such as system permission...'

    def handle(self, *args, **options):
        all_perm = AppConfig.get_all_permissions()
        logger.debug(str(all_perm))
        for one_perm in all_perm:
            context = ContentType.objects.filter(app_label=one_perm.PermissionApp).first()
            Permission.objects.update_or_create(content_type=context, name=one_perm.PermissionName, codename=one_perm.PermissionKey)
        AuthGroupExpander.init()
        users = AppUserModel.objects.filter(is_superuser=True).all()
        group = Group.objects.get(name='superuser')
        for user in users:
            user.groups.add(group)


