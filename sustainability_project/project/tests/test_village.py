from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from project.models import CustomUser, Challenge, DailyChallenge, UserChallenges
from django.utils.timezone import now
from django.contrib.auth.models import User


class TestVillage(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a CustomUser object
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            streak=5,
            best_streak=10,
            coins=100,
            score=100
        )
        # Log the user in
        self.client.login(username='testuser', password='testpass123')

    def test_success_buy_item(self):
        response = self.client.post(reverse('village', args=[self.user.username]), {'item': 'Tree', 'position': 1})

        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.user.coins, 50)
        self.assertEquals(self.user.score, 200)

        messages = list(get_messages(response.wsgi_request))
        print(messages)


    def test_not_afford_item(self):
        response = self.client.post(reverse('village', args=[self.user.username]), {'item': 'Phoenix King', 'position': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.user.coins, 100)
        self.assertEquals(self.user.score, 100)
    def test_wrong_item(self):
        response = self.client.post(reverse('village', args=[self.user.username]), {'item': 'Wrong', 'position': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.user.coins, 100)
        self.assertEquals(self.user.score, 100)





