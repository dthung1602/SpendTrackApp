from django.urls import path

from spendtrackapp.views.plan import *

app_name = 'plan'
urlpatterns = [
    path('', index, name='index'),
    path('add/', add, name='add'),
    path('delete/', delete, name='delete'),
    path('edit/', edit, name='edit'),
]
