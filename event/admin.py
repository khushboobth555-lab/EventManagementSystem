from django.contrib import admin
from .models import Event, Ticket, Equipment, FoodItem

# Register your models here
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Equipment)
admin.site.register(FoodItem)
