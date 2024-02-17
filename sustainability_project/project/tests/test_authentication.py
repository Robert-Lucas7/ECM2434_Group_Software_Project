from django.test import TestCase
from django.urls import reverse
from ..forms import Signup
from ..models import CustomUser


class BaseTest(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }

        self.bad_user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'firstpassword',
            'password2': 'secondpassword'
        }

        self.register_url = reverse('registration')
        self.login_url = reverse('login')
        self.home_url = reverse('home')

        self.register_template = 'project/registration.html'
        self.login_template = 'login.html'

        self.login_user_data = {
            'username': 'loginuser',
            'password': 'loginpassword'
        }

        self.bad_login_user_data = {
            'username': 'badloginuser',
            'password': 'badpassword'
        }
        self.user = CustomUser.objects.create_user(username=self.login_user_data['username'],
                                                   password=self.login_user_data['password'])


class SignUpTest(BaseTest):
    def test_access_signup_page(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.register_template)

    def test_signup_success(self):
        # get response object to registration post with user details
        response = self.client.post(self.register_url, data=self.user_data)

        # test for redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

        # Assert user object was created
        users = CustomUser.objects.filter(username='testuser')
        self.assertEquals(users.count(), 1)

    def test_signup_fail(self):
        # get response to incorrect registration post
        response = self.client.post(self.register_url, data=self.bad_user_data)

        self.assertEqual(response.status_code, 200)


class LoginTest(BaseTest):
    def test_access_login_page(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.login_template)

    def test_login_success(self):
        response = self.client.post(self.login_url, data=self.login_user_data)

        # assert redirected
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

        # test user logged in
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_fail(self):
        response = self.client.post(self.login_url, data=self.bad_login_user_data)

        # Not redirected
        self.assertEqual(response.status_code, 200)
