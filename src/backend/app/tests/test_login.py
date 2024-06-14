from typing import Tuple

from django.test import TestCase, Client
from django.urls import reverse, resolve
from public_tools.tools.read_env import GetEnv
from app.models.app_user import AppUserModel

from django.test import Client


class AuthorizedClient(Client):
    def __init__(self, *args, token=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token  # Store the token to be used in requests

    def generic(self, method, path, data='', content_type='application/octet-stream', secure=False, **extra):
        """
        Overridden method to add the Authorization header to every request.
        """
        if self.token and 'HTTP_AUTHORIZATION' not in extra:
            extra['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'

        return super().generic(method, path, data=data, content_type=content_type, secure=secure, **extra)

    def get(self, path, data='', follow=False, secure=False, **extra):
        """Overridden get method to utilize the modified generic method."""
        return self.generic('GET', path, data=data, follow=follow, secure=secure, **extra)

    def post(self, path, data='', content_type='application/octet-stream', follow=False, secure=False, **extra):
        """Overridden post method to utilize the modified generic method."""
        return self.generic('POST', path, data=data, content_type=content_type, follow=follow, secure=secure, **extra)
    # You can similarly override put(), delete(), etc., if needed.

def get_authorized_session(user_name=None, password=None) -> Tuple[int, AuthorizedClient]:
    AppUserModel.gen_default_super_user()
    if user_name is None or password is None:
        user_name = GetEnv().get_env().super_user_name
        password = GetEnv().get_env().super_user_password
    url = reverse('token_obtain_pair')
    login_data = {'username': user_name, 'password': password}
    client = Client()
    response = client.post(url, login_data)
    if response.status_code == 200:
        current_token = response.data['data']['access_token']
        print('client use the token is :', current_token)
        new_client = AuthorizedClient(token=current_token)
        return 200, new_client
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
        # test refresh token
        # response = session.post(reverse('token_refresh'), {'refresh': session.headers['refresh_token']})
        # self.assertEqual(response.status_code, 200)

    def test_user_recognition(self):
        response_code, session = get_authorized_session(self.test_super_user, self.test_super_user_password)
        self.assertEqual(response_code, 200)
        ret = session.get(reverse('appusermodel-get-user-info'))
        self.assertEqual(ret.status_code, 200)
        print(ret.json())
        self.assertEqual(ret.json()['data'], self.test_super_user)



