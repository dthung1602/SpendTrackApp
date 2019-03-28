from django.urls import path

from spendtrackapp.views.entry import *

app_name = 'entry'
urlpatterns = [
    path('add/', add_handler, name='add'),
    path('edit/', edit_handler, name='edit'),
    path('delete/', delete_handler, name='delete'),
]
