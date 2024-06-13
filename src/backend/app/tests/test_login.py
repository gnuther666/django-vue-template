from django.test import TestCase, Client
from django.urls import reverse, resolve
from public_tools.tools.read_env import GetEnv
from app.models.app_user import AppUserModel

def get_authorized_session(user_name=None, password=None):
    AppUserModel.gen_default_super_user()
    if user_name is None or password is None:
        user_name = GetEnv().get_env().super_user_name
        password = GetEnv().get_env().super_user_password
    url = reverse('token_obtain_pair')
    login_data = {'username': user_name, 'password': password}
    client = Client()
    response = client.post(url, login_data)
    if response.status_code == 200:
        print(response.data)
        auth_header = 'Bearer ' + response.data['data']['access_token']
        client.headers = {'Authorization': auth_header}
        return 200, client
    else:
        return response.status_code, None
class AnimalTestCase(TestCase):
    def setUp(self):
        self.test_super_user = GetEnv().get_env().super_user_name
        self.test_super_user_password = GetEnv().get_env().super_user_password
        self.client = None

    def test_login(self):
        # test_password error
        response_code, session  = get_authorized_session(self.test_super_user, '888888')
        self.assertEqual(response_code, 201)
        # test_login success
        response_code, session  = get_authorized_session(self.test_super_user, self.test_super_user_password)
        # Assert successful login (check status code or redirected URL)
        self.assertEqual(response_code, 200)


