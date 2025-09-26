from .models import Equipment
from .forms import EquipmentForm

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
from user.forms import UserForm, UpdateUserForm, ProfileForm, UpdateProfileForm, AddMoneyForm, WithdrawMoneyForm
from .models import Event, Ticket, FoodItem
from user.models import  Profile
from .forms import EventForm, BuyTicketForm, FoodItemForm


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg', 'webp']

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)

def home(request):
    if not request.user.is_authenticated:
          return redirect('user:login_user')
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

def food_list(request):
    if not request.user.is_superuser:
        return redirect('user:login_user')
    foods = FoodItem.objects.all()
    return render(request, 'event/food_list.html', {'foods': foods})

def add_food_item(request):
    if not request.user.is_superuser:
        return redirect('user:login_user')
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.save()
            messages.success(request, 'Food item added successfully!')
            return redirect('event:food_list')
    else:
        form = FoodItemForm()
    return render(request, 'event/food_item_form.html', {'form': form})

def update_food_item(request, pk):
    if not request.user.is_superuser:
        return redirect('user:login_user')
    food_item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food item updated successfully!')
            return redirect('event:food_list')
    else:
        form = FoodItemForm(instance=food_item)
    return render(request, 'event/food_item_form.html', {'form': form})
def equipment_list(request):
    if not request.user.is_superuser:
        return redirect('user:login_user')
    equipments = Equipment.objects.all()
    return render(request, 'event/equipment_list.html', {'equipments': equipments})

def add_equipment(request):
    if not request.user.is_superuser:
        return redirect('user:login_user')
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.save()
            messages.success(request, 'Equipment added successfully!')
            return redirect('event:equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'event/equipment_form.html', {'form': form})

def update_equipment(request, pk):
    if not request.user.is_superuser:
        return redirect('user:login_user')
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment updated successfully!')
            return redirect('event:equipment_list')
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'event/equipment_form.html', {'form': form})

def detail(request, pk):
    if not request.user.is_authenticated:
        return redirect('user:login_user')
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
                form.save_m2m()  # Save ManyToMany relationships (foods)
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


def buy_ticket(request, pk):
    user = request.user
    event = Event.objects.get(id=pk)
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = BuyTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Check if user already has a ticket for this event
            if Ticket.objects.filter(attendee=user, event=event).exists():
                error_message = 'You have already purchased a ticket for this event.'
                return render(request, 'event/buy_ticket.html', {
                    'profile': profile, 'form': form, 'event': event, 'error_message': error_message
                })
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
                return redirect('user:profile')
            context = {'profile': profile, 'form': form, 'event': event, 'error_message': 'Invalid Pin!'}
            return render(request, 'event/buy_ticket.html', context)
    else:
        form = BuyTicketForm()
    return render(request, 'event/buy_ticket.html', {'profile': profile, 'form': form, 'event': event})


def invite_users(request, pk):
    all_users = User.objects.all()
    event = Event.objects.get(id=pk)
    # Only users who have NOT bought a ticket (flag=True) for this event
    ticket_buyers = [t.attendee for t in Ticket.objects.filter(event=event, flag=True)]
    invited_users = [t.attendee for t in Ticket.objects.filter(event=event, flag=False)]
    # Exclude manager, ticket buyers, and already invited users
    users = list(set(all_users) - set(ticket_buyers) - set(invited_users) - {event.manager})
    context = {'users': users, 'event': event}
    return render(request, 'event/invite_users.html', context)


def send_invites(request, pk):
    all_users = User.objects.all()
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
