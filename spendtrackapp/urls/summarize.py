from django.urls import path

from spendtrackapp.views.summarize import *
# noinspection PyUnresolvedReferences
from . import converters

urlpatterns = [
    path('<yyyy:year>', year_handler, name='summarize_year'),
    path('<yyyy:year>/<mmm:month>', month_handler, name='summarize_month'),
    path('<yyyy:year>/<ww:week>', week_handler, name='summarize_week'),
    path('<date:start_date>/<date:end_date>', date_range_handler, name='summarize_date_range'),
]
