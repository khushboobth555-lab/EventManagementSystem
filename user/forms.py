from django import forms
from django.contrib.auth.models import User
from .models import Profile
from datetime import date

class UserForm(forms.ModelForm):
	username = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput, required=True)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'first_name', 'last_name']

class ProfileForm(forms.ModelForm):
	wallet_pin = forms.CharField(
		widget=forms.PasswordInput(attrs={'inputmode': 'numeric', 'maxlength': '4', 'minlength': '4'}),
		required=True,
		min_length=4,
		max_length=4,
		label='Wallet PIN',
		help_text='Enter a 4-digit number.'
	)
	bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 1}), required=False)
	location = forms.CharField(widget=forms.Textarea(attrs={'rows': 1}), required=False)
	birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
	age = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly': 'readonly'}), required=False)

	def clean_wallet_pin(self):
		pin = self.cleaned_data.get('wallet_pin')
		if not pin.isdigit() or len(pin) != 4:
			raise forms.ValidationError('Wallet PIN must be a 4-digit number.')
		return pin

	def clean(self):
		cleaned_data = super().clean()
		birth_date = cleaned_data.get('birth_date')
		if birth_date:
			today = date.today()
			age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
			cleaned_data['age'] = age
			if age < 18:
				self.add_error('birth_date', 'You must be at least 18 years old to register.')
		return cleaned_data

	class Meta:
		model = Profile
		fields = [ 'birth_date', 'age', 'wallet_pin', 'image', 'bio', 'location']

class UpdateUserForm(forms.ModelForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)

	class Meta:
		model = User
		fields = [ 'email', 'first_name', 'last_name']

class UpdateProfileForm(forms.ModelForm):
	bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
	location = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
	birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
	age = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly': 'readonly'}), required=False)

	def clean(self):
		cleaned_data = super().clean()
		birth_date = cleaned_data.get('birth_date')
		if birth_date:
			today = date.today()
			age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
			cleaned_data['age'] = age
			if age < 18:
				self.add_error('birth_date', 'You must be at least 18 years old to register.')
		return cleaned_data

	class Meta:
		model = Profile
		fields = [ 'birth_date', 'age', 'image', 'bio', 'location']

class AddMoneyForm(forms.Form):
	amount = forms.IntegerField(label='Amount to Add', min_value=0)
	pin = forms.CharField(label='Enter PIN', widget=forms.PasswordInput)

class WithdrawMoneyForm(forms.Form):
	amount = forms.IntegerField(label='Amount to Withdraw', min_value=0)
	pin = forms.CharField(label='Enter PIN', widget=forms.PasswordInput)
