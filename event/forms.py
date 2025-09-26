from django import forms
from django.contrib.auth.models import User
from .models import Event, Ticket
from user.models import  Profile
from datetime import date
from .models import Event, Ticket, FoodItem


class EventForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'maxlength': '50'}))
    location = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'maxlength': '500'}), required=True)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)

    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    fare = forms.CharField(widget=forms.NumberInput(attrs={'inputmode': 'numeric' }), required=True )
    image = forms.ImageField(required=True)
    foods = forms.ModelMultipleChoiceField(
        queryset=FoodItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Available Foods'
    )

    class Meta:
        model = Event
        fields = ['name', 'location', 'date', 'time', 'fare', 'image','foods']

class FoodItemForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'maxlength': '100'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=True)
    price = forms.DecimalField(required=True, max_digits=7, decimal_places=2)
    image = forms.ImageField(required=True)

    class Meta:
        model = FoodItem
        fields = ['name', 'description', 'price', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError('Image is required.')
        if hasattr(image, 'content_type'):
            if image.content_type not in ['image/jpeg','image/jpg', 'image/png', 'image/webp']:
                raise forms.ValidationError('Only JPEG, JPG, PNG, and WEBP images are allowed.')
        return image


class BuyTicketForm(forms.Form):
    pin = forms.CharField(label='Enter PIN', widget=forms.PasswordInput)
