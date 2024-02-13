from django.db import models


class User(models.Model):

    def __str__(self):
        return self.username

    username = models.CharField(max_length=30, unique=True, null=False, blank=False)

    # need to store this as a hash
    password = models.CharField(null=False, blank=False, max_length=40)

    email = models.EmailField(null=False, blank=False)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    streak = models.IntegerField(default=0)

# Create your models here.
