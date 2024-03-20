from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class VillageShop(models.Model):
    item = models.CharField(max_length=25) #The item in the village.
    cost = models.PositiveIntegerField() #The cost of the item.
    max_quantity = models.PositiveIntegerField()
    image_name = models.CharField(max_length=50, default="")
    score = models.IntegerField(default=0)  # Add this line for the score of each item
    def __str__(self):
        return self.item
    
class CustomUser(AbstractUser):
    streak = models.PositiveIntegerField(default=0)
    best_streak =  models.PositiveIntegerField(default=0)
    coins = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0)  # Add this line for the score of each item
    profile_picture = models.CharField(max_length=25, default="blank.jpeg")
    is_gamekeeper = models.BooleanField(default=False)

class Village(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  #The user that the village items are for.
    item = models.ForeignKey(VillageShop, on_delete=models.CASCADE) #Details on how much the items cost and the maximum number of them allowed.
    purchased = models.DateTimeField(default=now()) #When the item was purchased
    # item_number = models.PositiveIntegerField() #The occurrence number of that item (e.g. tree0, tree1, tree2, etc)
    position = models.PositiveIntegerField() # Position must be positive or zero.
    def __self__(self):
        return f"{self.user.username} - {self.item} - {self.position}"
# Create your models here.


class Challenge(models.Model):
    title = models.CharField(max_length=70, primary_key=True, default="")      
    description = models.CharField(max_length=500, null=False)
    location_lat = models.DecimalField(max_digits=10,decimal_places = 8, null=True)
    location_long = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    def __str__(self):
        return self.title
    
class DailyChallenge(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    assigned = models.DateTimeField(default=now(), null=True)


class UserChallenges(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Set these as composite primary keys
    daily_challenge = models.ForeignKey(DailyChallenge, on_delete=models.CASCADE)
    submitted = models.DateTimeField(default=now())
    completed = models.BooleanField(default=False)
    response = models.CharField(max_length=250)
    points = models.PositiveIntegerField(default=0)
    user_lat = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    user_long = models.DecimalField(max_digits=11, decimal_places=8, null=True)



