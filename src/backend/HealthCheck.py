import os, sys
class CheckHealth:
    @staticmethod
    def run():
        has_error = False
        has_error = has_error or CheckHealth.check_django_status()
        return has_error


    @staticmethod
    def check_django_status():
        ret = os.system('python3 manage.py check')
        if ret != 0:
            print('ERROR: django 内部错误')
            return False
        return True

if __name__ == '__main__':
    ret = CheckHealth.run()
    if ret:
        sys.exit(1)
    else:
        sys.exit(0)