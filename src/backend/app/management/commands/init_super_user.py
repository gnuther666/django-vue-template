from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'init or reinit super user'

    def handle(self, *args, **options):
        from app.models.app_user import AppUserModel
        AppUserModel.gen_default_super_user()