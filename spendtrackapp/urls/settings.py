from django.urls import path

from spendtrackapp.views.settings import *

urlpatterns = [
    path('', index, name='settings_index'),
    path('edit/', edit, name='settings_edit'),
]
