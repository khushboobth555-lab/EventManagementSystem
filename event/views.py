from django.urls import reverse

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import update_session_auth_hash


from django.contrib import messages


from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.http import HttpResponse
from datetime import date
import datetime
import json

from .models import Event, Profile, Ticket
from .forms import EventForm, UserForm, UpdateUserForm,ProfileForm ,UpdateProfileForm,AddMoneyForm, WithdrawMoneyForm, BuyTicketForm

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg', 'webp']

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'event/login.html')
    events = Event.objects.all()
    query = request.GET.get("query")
    if query:
        events = events.filter(
            Q(name__icontains=query) |
            Q(manager__first_name__icontains=query) |
            Q(manager__last_name__icontains=query)
        ).distinct()
    return render(request, 'event/home.html', {
        'user': request.user,
        'events': events,
        'query': query,
    })


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
            return render(request, 'event/register.html', context)

        profile.save()
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            events = Event.objects.all()
            return render(request, 'event/home.html', {'events': events, 'user': user})
    return render(request, 'event/register.html', {
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
            return render(request, 'event/login.html', {'error_message': 'Your account has been disabled'})
        return render(request, 'event/login.html', {'error_message': 'Invalid login'})
    return render(request, 'event/login.html')


def get_user_profile(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('event:login_user')
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    tickets = Ticket.objects.filter(attendee=user)
    return render(request, 'event/user_profile.html', {'user': user, 'profile': profile, 'tickets': tickets})

def update_profile(request):
    if not request.user.is_authenticated:
        return redirect('event:login_user')
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
                return render(request, 'event/update_profile.html', context)

            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('event:user_profile')
    else:
        user_form = UpdateUserForm(instance=user, prefix="user")
        profile_form = UpdateProfileForm(instance=profile, prefix="profile")

    return render(request, 'event/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def logout_user(request):
    logout(request)
    return render(request, 'event/login.html')


def detail(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'event/login.html')
    user = request.user
    event = get_object_or_404(Event, pk=pk)
    tickets = Ticket.objects.filter(event=event)
    return render(request, 'event/detail.html', {'event': event, 'user': user, 'tickets': tickets})


def add_event(request):
    if not request.user.is_superuser:
        return render(request, '403.html', status=403)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.manager = request.user
            image = form.cleaned_data.get('image')
            if image:
                file_type = event.image.url.split('.')[-1].lower()
                if file_type not in IMAGE_FILE_TYPES:
                    return render(request, 'event/event_form.html', {
                        'form': form,
                        'error_message': 'Image file must be PNG, JPG, WebP or JPEG',
                    })
                event.save()
                return redirect(reverse('event:detail', kwargs={'pk': event.pk}))
        return render(request, 'event/event_form.html', {'form': form})
    else:
        form = EventForm()
        return render(request, 'event/event_form.html', {'form': form})

class EventUpdate(UpdateView):
    model = Event
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request, '403.html', status=403)
        pk = kwargs.get('pk')
        event = get_object_or_404(Event, pk=pk)
        form = self.form_class(instance=event)
        user = request.user
        return render(request, 'event/event_form.html', {
            'form': form,
            'event': event
        })
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return render(request, '403.html', status=403)
        pk = kwargs.get('pk')
        event = get_object_or_404(Event, pk=pk)
        form = self.form_class(request.POST, request.FILES, instance=event)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            if image:
                file_type = image.name.split('.')[-1].lower()
                if file_type not in IMAGE_FILE_TYPES:
                    context = {
                        'form': form,
                        'event': event,
                        'error_message': 'Image file must be PNG, JPG, WebP or JPEG',
                    }
                    return render(request, 'event/event_form.html', context)
            form.save()
            return redirect(reverse('event:detail', kwargs={'pk': event.pk}))
        return render(request, 'event/event_form.html', {
            'form': form,
            'event': event          
        })

def get_past_events(request):
    events = Event.objects.filter(date__lt=date.today())
    return render(request, 'event/get_past_events.html', {'events': events})


def add_money(request):
    if not request.user.is_authenticated:
        return redirect('event:login_user')
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
                return render(request, 'event/user_profile.html', {
                    'user': user, 'profile': profile, 'tickets': tickets
                })
            context = {'profile': profile, 'form': form, 'error_message': 'Invalid Pin!'}
            return render(request, 'event/add_money.html', context)
    else:
        form = AddMoneyForm()
    return render(request, 'event/add_money.html', {'profile': profile, 'form': form})


def withdraw_money(request):
    if not request.user.is_authenticated:
        return redirect('event:login_user')
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
                    return render(request, 'event/withdraw_money.html', context)
                profile.wallet_balance -= data['amount']
                profile.save()
                tickets = Ticket.objects.filter(attendee=request.user)
                return render(request, 'event/user_profile.html', {
                    'user': request.user, 'profile': profile, 'tickets': tickets
                })
            context = {'profile': profile, 'form': form, 'error_message': 'Invalid Pin!'}
            return render(request, 'event/withdraw_money.html', context)
    else:
        form = WithdrawMoneyForm()
    return render(request, 'event/withdraw_money.html', {'profile': profile, 'form': form})


def buy_ticket(request, pk):
    user = request.user
    event = Event.objects.get(id=pk)
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = BuyTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if int(data['pin']) == profile.wallet_pin:
                if event.fare > profile.wallet_balance:
                    error_balance = 'Insufficient balance to buy ticket'
                    return render(request, 'event/buy_ticket.html', {
                        'profile': profile, 'form': form, 'event': event, 'error_balance': error_balance
                    })
                Ticket.objects.create(attendee=user, event=event, flag=True)
                profile.wallet_balance -= event.fare
                owner_profile = Profile.objects.get(user=event.manager)
                owner_profile.wallet_balance += event.fare
                profile.save()
                owner_profile.save()
                tickets = Ticket.objects.filter(attendee=request.user)
                return render(request, 'event/user_profile.html', {
                    'user': user, 'profile': profile, 'tickets': tickets
                })
            context = {'profile': profile, 'form': form, 'event': event, 'error_message': 'Invalid Pin!'}
            return render(request, 'event/buy_ticket.html', context)
    else:
        form = BuyTicketForm()
    return render(request, 'event/buy_ticket.html', {'profile': profile, 'form': form, 'event': event})


def invite_users(request, pk):
    all_users = User.objects.filter(is_superuser=False)
    event = Event.objects.get(id=pk)
    attendees = [t.attendee for t in Ticket.objects.filter(event=event)]
    attendees.append(request.user)
    users = list(set(all_users) - set(attendees))
    context = {'users': users, 'event': event}
    return render(request, 'event/invite_users.html', context)


def send_invites(request, pk):
    all_users = User.objects.filter(is_superuser=False)
    event = Event.objects.get(id=pk)
    attendees = [t.attendee for t in Ticket.objects.filter(event=event)]
    attendees.append(request.user)
    users = list(set(all_users) - set(attendees))
    if request.method == 'POST':
        for user in users:
            if request.POST.get(user.username) == 'yes':
                Ticket.objects.create(attendee=user, event=event, flag=False)
        return redirect(reverse('event:detail', kwargs={'pk': event.pk}))


def event_name_validate(request):
    user = request.user
    name = request.GET.get('name')
    event_names = [e.name for e in Event.objects.filter(manager=user)]
    if name in event_names:
        return HttpResponse(json.dumps({'valid': 'false'}), content_type="application/json")
    return HttpResponse(json.dumps({'valid': 'true'}), content_type="application/json")


def event_date_validate(request):
    inp_date = request.GET.get('date')
    if inp_date:
        # HTML date input returns 'YYYY-MM-DD'
        try:
            inp_date = datetime.datetime.strptime(inp_date, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponse(json.dumps({'valid': 'false'}), content_type="application/json")
        # if inp_date < date.today():
        #     return HttpResponse(json.dumps({'valid': 'false'}), content_type="application/json")
    return HttpResponse(json.dumps({'valid': 'true'}), content_type="application/json")

def custom_bad_request(request, exception=None):
    return render(request, "400.html", status=400)

def custom_permission_denied(request, exception=None):
    return render(request, "403.html", status=403)

def custom_page_not_found(request, exception=None):
    return render(request, "404.html", status=404)

def custom_server_error(request):
    return render(request, "500.html", status=500)

# Change Password View
def change_password(request):
    if not request.user.is_authenticated:
        return redirect('event:login_user')
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
            return redirect('event:user_profile')
    return render(request, 'event/change_password.html', {'error_message': error_message})
# Change Wallet Pin View
# Change Wallet Pin View
def change_wallet_pin(request):
    if not request.user.is_authenticated:
        return redirect('event:login_user')
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
                return redirect('event:user_profile')           
    return render(request, 'event/change_wallet_pin.html', {'error_message': error_message})
