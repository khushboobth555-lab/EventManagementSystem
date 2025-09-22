from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.conf.urls import handler404

app_name = 'event'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    #path('add_event/', views.add_event, name='add_event'),
    re_path(r'^detail/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    re_path(r'^update/(?P<pk>[0-9]+)/$', views.EventUpdate.as_view(), name='update_event'),
    path('profile/', views.get_user_profile, name='user_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/change_password/', views.change_password, name='change_password'),
    path('profile/change_wallet_pin/', views.change_wallet_pin, name='change_wallet_pin'),
    path('past_events/', views.get_past_events, name='past_events'),
    path('add_money/', views.add_money, name='add_money'),
    path('withdraw_money/', views.withdraw_money, name='withdraw_money'),
    re_path(r'^buy_ticket/(?P<pk>[0-9]+)/$', views.buy_ticket, name='buy_ticket'),
    re_path(r'^invite_users/(?P<pk>[0-9]+)/$', views.invite_users, name='invite_users'),
    re_path(r'^send_invites/(?P<pk>[0-9]+)/$', views.send_invites, name='send_invites'),
    path('event_name_validate/', views.event_name_validate, name='event_name_validate'),
    path('event_date_validate/', views.event_date_validate, name='event_date_validate'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom 404 handler
handler404 = 'event.views.custom_404_view'

# Catch-all pattern for unmatched URLs
from django.urls import re_path
urlpatterns += [
    re_path(r'^.*$', views.custom_404_view),
]
