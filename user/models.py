from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver



# Custom User model with mobile_number field
from django.core.validators import RegexValidator



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{10}$', message='Mobile number must be exactly 10 digits.')],
        blank=True,
        null=True
    )
    image = models.ImageField(default='settings.MEDIA_ROOT/default_user.jpg')
    bio = models.TextField(max_length=500, blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    wallet_pin = models.PositiveIntegerField(null=True)
    wallet_balance = models.PositiveIntegerField(default=0, null=True)

    def __str__(self):
        return self.user.username
