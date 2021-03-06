from django.urls import path

from spendtrackapp.views.account import *

app_name = 'account'
urlpatterns = [
    path('', index, name='index'),
    path('register/', register_handler, name='register'),
    path('login/', login_handler, name='login'),
    path('logout/', logout_handler, name='logout'),
    path('edit/', edit_handler, name='edit'),
    path('delete/', delete_handler, name='delete'),
    path('password_change/', password_change_handler, name='password_change'),
    path('password_reset/', password_reset_handler, name='password_reset'),
    path('password_reset/confirm/<uidb64>/<token>/', password_reset_confirm_handler, name='password_reset_confirm')
]
