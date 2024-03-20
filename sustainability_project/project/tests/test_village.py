from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from project.models import CustomUser, Challenge, DailyChallenge, UserChallenges, VillageShop
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

        shop_item1 = {"item": "item1", "cost": 100, "image_name": "", "score": 100}
        shop_item2 = {"item": "item1", "cost": 1000, "image_name": "", "score": 100}

        self.item1 = VillageShop(item="item1", cost=100, image_name="", score=100)
        self.item1.save()

        self.item2 = VillageShop(item="item2", cost=1000, image_name="", score=100)
        self.item2.save()

        # Log the user in
        self.client.login(username='testuser', password='testpass123')

    def test_success_buy_item(self):
        print(VillageShop)
        response = self.client.post(reverse('village', args=[self.user.username]), {'item': 'item1', 'position': 1})
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.user.coins, 0)
        self.assertEquals(self.user.score, 200)

    def test_not_afford_item(self):
        response = self.client.post(reverse('village', args=[self.user.username]), {'item': 'Phoenix King', 'position': 1})
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.user.coins, 100)
        self.assertEquals(self.user.score, 100)

    def test_wrong_item(self):
        response = self.client.post(reverse('village', args=[self.user.username]), {'item': 'Wrong', 'position': 1})
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.user.coins, 100)
        self.assertEquals(self.user.score, 100)





