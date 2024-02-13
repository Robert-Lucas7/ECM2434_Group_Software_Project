from django.db import models


class User(models.Model):

    def __str__(self):
        return self.username

    username = models.CharField(max_length=30, unique=True, null=False, blank=False, primary_key=True)

    # need to store this as a hash
    password = models.CharField(null=False, blank=False, max_length=40)

    email = models.EmailField(null=False, blank=False)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    streak = models.IntegerField(default=0)
    #challenges_completed = models.ManyToManyField("Challenge", related_name="user")

# Create your models here.



class Challenge(models.Model):
    title = models.CharField(max_length=70, primary_key=True, default="")


    def __str__(self):
        return self.title
        #return self.username
    
    #username = models.CharField(max_length=50, unique=True, null=False)

    info = models.CharField(max_length=500, unique=True, null=False)
    #num_completed = models.IntegerField(default=0)
    #date = models.DateField()

class UserChallenges(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #Set these as composite primary keys
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date= models.DateField()

class ChallengesAssigned(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date_assigned = models.DateField(null=False)

    
