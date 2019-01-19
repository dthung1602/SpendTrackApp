from django.urls import path

from spendtrackapp.views.summarize import *
# noinspection PyUnresolvedReferences
from . import converters

app_name = 'summarize'
urlpatterns = [
    path('', index, name='index'),

    path('<yyyy:year>', year_handler, name='year'),
    path('<yyyy:year>/<mmm:month>', month_handler, name='month'),
    path('<yyyy:year>/w<ww:week>', week_handler, name='week'),
    path('<date:start_date>/<date:end_date>', date_range_handler, name='date_range'),

    path('today', today_handler, name='today'),
    path('this-week', this_week_handler, name='this_week'),
    path('this-month', this_month_handler, name='this_month'),
    path('this-year', this_year_handler, name='this_year')
]
