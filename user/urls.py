from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register, name='register'),
    path('profile/', views.get_user_profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/change_password/', views.change_password, name='change_password'),
    path('profile/change_wallet_pin/', views.change_wallet_pin, name='change_wallet_pin'),
    path('add_money/', views.add_money, name='add_money'),
    path('withdraw_money/', views.withdraw_money, name='withdraw_money'),
]
