# Code by Ben
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

# Items in the village shop
class VillageShop(models.Model):
    item = models.CharField(max_length=25) 
    cost = models.PositiveIntegerField() 
    image_name = models.CharField(max_length=50, default="")
    score = models.IntegerField(default=0)  

    def __str__(self):
        return self.item
    
# Users of the app
class CustomUser(AbstractUser):
    streak = models.PositiveIntegerField(default=0)
    best_streak =  models.PositiveIntegerField(default=0)
    coins = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0) 
    profile_picture = models.CharField(max_length=25, default="blank.jpeg")
    is_gamekeeper = models.BooleanField(default=False)

# Village of a user
class Village(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    item = models.ForeignKey(VillageShop, on_delete=models.CASCADE) 
    purchased = models.DateTimeField(default=now)
    position = models.PositiveIntegerField() 
    def __self__(self):
        return f"{self.user.username} - {self.item} - {self.position}"

# Challenges in the app
class Challenge(models.Model):
    title = models.CharField(max_length=70, primary_key=True, default="")      
    description = models.CharField(max_length=500, null=False)
    location_lat = models.DecimalField(max_digits=10,decimal_places = 8, null=True)
    location_long = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    def __str__(self):
        return self.title
    
# Challenges assigned on a specific day is stored as a daily challenge
class DailyChallenge(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    assigned = models.DateTimeField(default=now, null=True)

# User's response to a daily challenge
class UserChallenges(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  
    daily_challenge = models.ForeignKey(DailyChallenge, on_delete=models.CASCADE)
    submitted = models.DateTimeField(default=now)
    completed = models.BooleanField(default=False)
    response = models.CharField(max_length=250)
    points = models.PositiveIntegerField(default=0)
    user_lat = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    user_long = models.DecimalField(max_digits=11, decimal_places=8, null=True)
