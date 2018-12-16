from django.urls import path

from spendtrackapp.views.plan import *

app_name = 'plan'
urlpatterns = [
    path('', index_handler, name='index'),
    path('search/', search_handler, name='search'),
    path('add/', add_handler, name='add'),
    path('delete/', delete_handler, name='delete'),
    path('edit/', edit_handler, name='edit'),
]
