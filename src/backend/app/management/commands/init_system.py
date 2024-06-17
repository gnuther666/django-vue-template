from django.core.management.base import BaseCommand
from app.apps import AppConfig
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from app.Permissions import AppPermissions
class Command(BaseCommand):
    help = 'init such as system permission...'

    def handle(self, *args, **options):
        app_name = AppConfig.name
        context = ContentType.objects.filter(app_label=app_name).first()
        for one_perm in AppPermissions:
            Permission.objects.update_or_create(content_type=context, name=one_perm.value, codename=one_perm.name)

