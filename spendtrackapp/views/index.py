from django.shortcuts import render

from spendtrackapp.models import *


def index(request):
    current_balance = Info.get('CURRENT_BALANCE')
    category_tree = Category.get_tree()
    now = datetime.now()
    isoyear, week, week_day = now.isocalendar()
    entries_in_week = Entry.find_by_week(isoyear, week)
    total_in_week = Entry.total_by_week(isoyear, week)
    context = {
        'current_balance': current_balance,
        'category_tree': category_tree,
        'now': now,
        'entries_in_week': entries_in_week,
        'total_in_week': total_in_week
    }
    return render(request, 'spendtrackapp/index.html', context)
