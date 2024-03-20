from django.test import TestCase, Client
from django.urls import reverse
from project.models import CustomUser, Challenge, DailyChallenge, UserChallenges
from django.utils.timezone import now

class TestUserProfile(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a CustomUser object
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            streak=5,
            best_streak=10,
            coins=100,
            profile_picture = "dog.jpeg"
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

    def test_change_profile_picture(self):

        response = self.client.post(reverse('change_profile_picture'), {'profile_picture': "cat.jpeg"})

        self.assertEquals(CustomUser.profile_picture, "cat.jpeg")

    def test_change_profile_picture_stays_same(self):

        response = self.client.post(reverse('change_profile_picture'), {'profile_picture': "Select Profile Picture"})

        self.assertEquals(CustomUser.profile_picture, "cat.jpeg")
    