from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class TestUserLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login') 
        self.register_url = reverse('registration') 
        self.UserModel = get_user_model()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@exeter.ac.uk',
            'password1': 'testpassword1',
            'password2': 'testpassword1',
        }

    
    def test_can_register_user_with_valid_data(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertEqual(self.UserModel.objects.count(), 1)  # A user was created


    def test_cannot_register_user_with_invalid_email(self):
        self.user_data['email'] = 'testuser@gmail.com'
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 200)  # Stays on the same page
        self.assertEqual(self.UserModel.objects.count(), 0)  # No user was created


    def test_cannot_register_user_with_short_password(self):
        self.user_data['password1'] = 'test'
        self.user_data['password2'] = 'test'
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 200)  # Stays on the same page
        self.assertEqual(self.UserModel.objects.count(), 0)  # No user was created


    def test_can_login_with_valid_credentials(self):
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword1',
        })
        user = self.UserModel.objects.get(username='testuser')
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)  # User is logged in


    def test_cannot_login_with_invalid_credentials(self):
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)  # Stays on the same page
        self.assertNotIn('_auth_user_id', self.client.session)  # User is not logged in


    def test_cannot_register_with_duplicate_username_or_email(self):
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 200)  # Stays on the same page
        self.assertEqual(self.UserModel.objects.count(), 1)  # No additional user was created


    def test_cannot_register_with_unmatched_passwords(self):
        self.user_data['password2'] = 'differentpassword'
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 200)  # Stays on the same page
        self.assertEqual(self.UserModel.objects.count(), 0)  # No user was created


    def test_can_logout(self):
        self.client.post(self.register_url, self.user_data)
        self.client.login(username='testuser', password='testpassword1')
        response = self.client.get(reverse('logout'))  
        self.assertEqual(response.status_code, 302)  # Redirect after successful logout
        self.assertNotIn('_auth_user_id', self.client.session)  # User is not logged in
    

    def test_anonymous_user_cannot_access_protected_view(self):
        response = self.client.get(reverse('home'))  
        self.assertEqual(response.status_code, 302)  # Redirect to login page