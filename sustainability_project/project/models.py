from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    streak = models.PositiveIntegerField(default=0)
    # challenges_completed = models.ManyToManyField("Challenge", related_name="user")


# Create your models here.


class Challenge(models.Model):
    title = models.CharField(max_length=70, primary_key=True, default="")

    def __str__(self):
        return self.title
        # return self.username

    # username = models.CharField(max_length=50, unique=True, null=False)

    info = models.CharField(max_length=500, unique=True, null=False)
    # num_completed = models.IntegerField(default=0)
    # date = models.DateField()


class UserChallenges(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Set these as composite primary keys
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date = models.DateField()


class ChallengesAssigned(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date_assigned = models.DateField(null=False)
