from django.contrib import admin
from .models import Profile, WalletTransaction
# Register user-related models here
admin.site.register(Profile)
admin.site.register(WalletTransaction)
