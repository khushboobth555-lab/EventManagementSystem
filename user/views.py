from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import date
from .models import Profile
from .forms import UserForm, ProfileForm, UpdateUserForm, UpdateProfileForm, AddMoneyForm, WithdrawMoneyForm

from event.models import Ticket
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg', 'webp']

def register(request):
    register_form = UserForm(request.POST or None, prefix="user")
    profile_form = ProfileForm(request.POST or None, request.FILES or None, prefix="profile")
    if register_form.is_valid() and profile_form.is_valid():
        user = register_form.save(commit=False)
        username = register_form.cleaned_data['username']
        password = register_form.cleaned_data['password']
        user.set_password(password)
        user.save()

        profile = profile_form.save(commit=False)
        profile.user = user
        profile.wallet_balance = 0
        profile.image = profile_form.cleaned_data['image']

        file_type = profile.image.url.split('.')[-1].lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'register_form': register_form,
                'profile_form': profile_form,
                'error_message': 'Image file must be PNG, JPG, WebP or JPEG',
            }
            return render(request, 'user/register.html', context)

        profile.save()
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return redirect('user:profile')
    return render(request, 'user/register.html', {
        "register_form": register_form,
        "profile_form": profile_form,
    })


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('event:home')
            return render(request, 'user/login.html', {'error_message': 'Your account has been disabled'})
        return render(request, 'user/login.html', {'error_message': 'Invalid login'})
    return render(request, 'user/login.html')


def get_user_profile(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('user:login_user')
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    tickets = Ticket.objects.filter(attendee=user)
    return render(request, 'user/user_profile.html', {'user': user, 'profile': profile, 'tickets': tickets})

def update_profile(request):
    if not request.user.is_authenticated:
        return redirect('user:login_user')
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user, prefix="user")
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile, prefix="profile")
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile.image = profile_form.cleaned_data['image']

            file_type = profile.image.url.split('.')[-1].lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'user_form': user_form,
                    'profile_form': profile_form,
                    'error_message': 'Image file must be PNG, JPG, WebP or JPEG',
                 }
                return render(request, 'user/update_profile.html', context)

            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user:profile')
    else:
        user_form = UpdateUserForm(instance=user, prefix="user")
        profile_form = UpdateProfileForm(instance=profile, prefix="profile")

    return render(request, 'user/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def logout_user(request):
    logout(request)
    return render(request, 'user/login.html')

def add_money(request):
    if not request.user.is_authenticated:
        return redirect('user:login_user')
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        form = AddMoneyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if int(data['pin']) == profile.wallet_pin:
                profile.wallet_balance += data['amount']
                profile.save()
                tickets = Ticket.objects.filter(attendee=request.user)
                return render(request, 'user/user_profile.html', {
                    'user': user, 'profile': profile, 'tickets': tickets
                })
            context = {'profile': profile, 'form': form, 'error_message': 'Invalid Pin!'}
            return render(request, 'user/add_money.html', context)
    else:
        form = AddMoneyForm()
    return render(request, 'user/add_money.html', {'profile': profile, 'form': form})


def withdraw_money(request):
    if not request.user.is_authenticated:
        return redirect('user:login_user')
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        form = WithdrawMoneyForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if int(data['pin']) == profile.wallet_pin:
                if data['amount'] > profile.wallet_balance:
                    context = {
                        'profile': profile,
                        'form': form,
                        'error_message': 'Amount to withdraw cannot be more than available balance'
                    }
                    return render(request, 'user/withdraw_money.html', context)
                profile.wallet_balance -= data['amount']
                profile.save()
                tickets = Ticket.objects.filter(attendee=request.user)
                return render(request, 'user/user_profile.html', {
                    'user': request.user, 'profile': profile, 'tickets': tickets
                })
            context = {'profile': profile, 'form': form, 'error_message': 'Invalid Pin!'}
            return render(request, 'user/withdraw_money.html', context)
    else:
        form = WithdrawMoneyForm()
    return render(request, 'user/withdraw_money.html', {'profile': profile, 'form': form})

# Change Password View
def change_password(request):
    if not request.user.is_authenticated:
        return redirect('user:login_user')
    error_message = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        user = request.user
        if not user.check_password(old_password):
            error_message = 'Current password is incorrect.'
        elif new_password1 != new_password2:
            error_message = 'New passwords do not match.'
        elif not new_password1 or len(new_password1) < 6:
            error_message = 'New password must be at least 6 characters.'
        else:
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('user:profile')
    return render(request, 'user/change_password.html', {'error_message': error_message})
# Change Wallet Pin View
# Change Wallet Pin View
def change_wallet_pin(request):
    if not request.user.is_authenticated:
        return redirect('user:login_user')
    error_message = None
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        old_pin = request.POST.get('old_pin')
        new_pin1 = request.POST.get('new_pin1')
        new_pin2 = request.POST.get('new_pin2')
        # Validate pins as strings before converting to int
        if not (old_pin and new_pin1 and new_pin2):
            error_message = 'All pin fields are required.'
        elif not (str(old_pin).isdigit() and str(new_pin1).isdigit() and str(new_pin2).isdigit()):
            error_message = 'Pins must be numeric.'
        elif not (len(str(new_pin1)) == 4 and len(str(new_pin2)) == 4):
            error_message = 'Pin must be a 4-digit number.'
        else:
            old_pin_int = int(old_pin)
            new_pin1_int = int(new_pin1)
            new_pin2_int = int(new_pin2)
            if old_pin_int != profile.wallet_pin:
                error_message = 'Current pin is incorrect.'
            elif new_pin1_int != new_pin2_int:
                error_message = 'New pins do not match.'
            else:
                profile.wallet_pin = new_pin1_int
                profile.save()
                messages.success(request, 'Wallet pin changed successfully.')
                return redirect('user:profile')           
    return render(request, 'user/change_wallet_pin.html', {'error_message': error_message})