from django.test import TestCase

# Create your tests here.

def auto_test():
    from app.models.app_user import AppUserModel
    AppUserModel.gen_default_super_user()

if __name__ == '__main__':
    auto_test()