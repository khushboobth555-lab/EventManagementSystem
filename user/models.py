from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='settings.MEDIA_ROOT/default_user.jpg')
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    wallet_pin = models.PositiveIntegerField(null=True)
    wallet_balance = models.PositiveIntegerField(default=0, null=True)

    def __str__(self):
        return self.user.username
