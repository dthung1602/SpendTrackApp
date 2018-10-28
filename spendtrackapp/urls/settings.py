from django.urls import path

from spendtrackapp.views.settings import *

app_name = 'settings'
urlpatterns = [
    path('', index, name='index'),
    path('edit/', edit, name='edit'),
]
