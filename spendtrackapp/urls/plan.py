from django.urls import path

from spendtrackapp.views.plan import *

urlpatterns = [
    path('', index, name='plan_index'),
    path('add/', add, name='plan_add'),
    path('delete/', delete, name='plan_delete'),
    path('edit/', edit, name='plan_edit'),
]
