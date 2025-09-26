from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.utils import timezone

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
# Wallet transaction table for wallet history
class WalletTransaction(models.Model):
    class Type(models.TextChoices):
        CREDIT = "credit", "Credit"
        DEBIT = "debit", "Debit"

    class Purpose(models.TextChoices):
        ADDED_MONEY = "added_money", "Added Money"
        CREDITED_ON_BOOKING = "credited_on_booking", "Money Credited on Ticket Booking"
        WITHDRAWAL = "withdrawal", "Withdrawal by User"
        TICKET_BOOKING = "ticket_booking", "Ticket Booking"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wallet_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=Type.choices)
    purpose = models.CharField(max_length=30, choices=Purpose.choices)
    reference = models.CharField(max_length=255, blank=True, null=True)
    event = models.ForeignKey('event.Event', on_delete=models.SET_NULL, blank=True, null=True)
    payment_reference = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    def save(self, *args, **kwargs):
        import random, string
        if not self.payment_reference:
            self.payment_reference = ''.join(random.choices(string.digits + string.ascii_uppercase, k=10))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.type} - {self.amount} - {self.purpose}"
