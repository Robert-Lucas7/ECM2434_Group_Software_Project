from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class CustomUser(AbstractUser):
    streak = models.PositiveIntegerField(default=0)
    best_streak =  models.PositiveIntegerField(default=0)
    #points = models.PositiveIntegerField(default=0)
    # challenges_completed = models.ManyToManyField("Challenge", related_name="user")


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
    # user_lat = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    # user_long = models.DecimalField(max_digits=11, decimal_places=8, null=True)


