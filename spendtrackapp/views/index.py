from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from spendtrackapp.models import *


@login_required
def index(request):
    current_balance = Info.get('CURRENT_BALANCE')
    root_categories = Category.get_root_categories()
    now = datetime.now()
    isoyear, week, week_day = now.isocalendar()
    entries_in_week = Entry.find_by_week(isoyear, week)
    total_in_week = Entry.total_by_week(isoyear, week)
    context = {
        'current_balance': current_balance,
        'root_categories': root_categories,
        'now': now,
        'entries_in_week': entries_in_week,
        'total_in_week': total_in_week
    }
    return render(request, 'spendtrackapp/index.html', context)
