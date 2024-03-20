# Code by Elliot
from django.test import TestCase, Client
from django.urls import reverse
from project.models import CustomUser, Challenge, DailyChallenge, UserChallenges
from django.utils.timezone import now

class TestUserChallenges(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a CustomUser object
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            streak=5,
            best_streak=10,
            coins=100
        )
        # Log the user in
        self.client.login(username='testuser', password='testpass123')

        # Create a Challenge object
        self.challenge = Challenge.objects.create(
            title='Test Challenge',
            description='Test description',
            location_lat=51.5074,
            location_long=0.1278
        )

        # Create a DailyChallenge object
        self.daily_challenge = DailyChallenge.objects.create(
            challenge=self.challenge,
            assigned=now()
        )

    def test_create_user_challenge(self):
        data = {
            'daily_challenge': self.daily_challenge.id,
            'comment': 'Test comment',
            'user_lat': 51.5074,
            'user_long': 0.1278
        }

        # Make the post request
        response = self.client.post(reverse('make_post'), data)
        if response.context and 'form' in response.context:
            print(response.context['form'].errors)

        # Check that the response has a status code of 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that a UserChallenges object was created
        self.assertEqual(UserChallenges.objects.count(), 1)

        # Check that the created UserChallenges object has the correct attributes
        user_challenge = UserChallenges.objects.first()
        self.assertEqual(user_challenge.daily_challenge, self.daily_challenge)
        self.assertEqual(user_challenge.response, 'Test comment')
        self.assertEqual(float(user_challenge.user_lat), 51.5074) 
        self.assertEqual(float(user_challenge.user_long), 0.1278)
    

    def test_create_user_challenge_with_invalid_data(self):
        data = {
            'daily_challenge': self.daily_challenge.id,
            'comment': '',
            'user_lat': 51.5074,
            'user_long': 0.1278
        }
        response = self.client.post(reverse('make_post'), data)
        self.assertEqual(response.status_code, 200)  # should render the form again
        self.assertEqual(UserChallenges.objects.count(), 0)  # no object should be created


    def test_create_user_challenge_unauthenticated(self):
        self.client.logout()  # log out the user
        data = {
            'daily_challenge': self.daily_challenge.id,
            'comment': 'Test comment',
            'user_lat': 51.5074,
            'user_long': 0.1278
        }
        response = self.client.post(reverse('make_post'), data)
        self.assertEqual(response.status_code, 302)  # should redirect to login page
        self.assertEqual(UserChallenges.objects.count(), 0)  # no object should be created
