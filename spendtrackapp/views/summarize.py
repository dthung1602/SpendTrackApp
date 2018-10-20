from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render

from spendtrackapp.models import Entry, Category


def get_date_range_total(start_date, end_date):
    total = float(Entry.total_by_date_range(start_date, end_date))
    category_total = {}
    for category in Category.objects.all():
        category_total[category.name] = float(
            Entry.total_by_date_range(start_date, end_date, category_name=category.name))
    return total, category_total


def get_year_total(y):
    total = float(Entry.total_by_year(y))
    category_total = {}
    for category in Category.objects.all():
        category_total[category.name] = float(Entry.total_by_year(y, category_name=category.name))
    return total, category_total


def get_month_total(y, m):
    total = float(Entry.total_by_month(y, m))
    category_total = {}
    for category in Category.objects.all():
        category_total[category.name] = float(Entry.total_by_month(y, m, category_name=category.name))
    return total, category_total


def get_week_total(y, w):
    total = float(Entry.total_by_week(y, w))
    category_total = {}
    for category in Category.objects.all():
        category_total[category.name] = float(Entry.total_by_week(y, w, category_name=category.name))
    return total, category_total


@login_required
def date_range(request, start_date, end_date):
    total, category_total = get_date_range_total(start_date, end_date)
    context = {
        'total': total,
        'category_total': category_total,
    }
    if request.is_ajax():
        return JsonResponse(context)

    entries = list(Entry.find_by_date_range(start_date, end_date))
    context.update({
        'entries': entries
    })
    return render(request, "spendtrackapp/summarize_date_range.html", context)


@login_required
def year(request, year):
    this_year_total, this_year_category_total = get_year_total(year)
    context = {
        'this_year_total': this_year_total,
        'this_year_category_total': this_year_category_total,
    }
    if request.is_ajax():
        return JsonResponse(context)

    entries = Entry.find_by_year(year)
    last_year_total, last_year_category_total = get_year_total(year - 1)
    context.update({
        'entries': entries,
        'last_year_total': last_year_total,
        'last_year_category_total': last_year_category_total
    })
    return render(request, "spendtrackapp/summarize_year.html", context)


@login_required
def month(request, year, month):
    this_month_total, this_month_category_total = get_month_total(year, month)
    context = {
        'this_month_total': this_month_total,
        'this_month_category_total': this_month_category_total,
    }
    if request.is_ajax():
        return JsonResponse(context)

    entries = Entry.find_by_month(year, month)
    month -= 1
    if month == 0:
        month = 12
        year -= 1
    last_month_total, last_month_category_total = get_month_total(year, month)
    context.update({
        'entries': entries,
        'last_month_total': last_month_total,
        'last_month_category_total': last_month_category_total
    })
    return render(request, "spendtrackapp/summarize_month.html", context)


@login_required
def week(request, year, week):
    this_week_total, this_week_category_total = get_week_total(year, week)
    context = {
        'this_week_total': this_week_total,
        'this_week_category_total': this_week_category_total,
    }
    if request.is_ajax():
        return JsonResponse(context)

    entries = Entry.find_by_week(year, week)
    week -= 1
    if week == 0:
        d = datetime(year, 1, 1)
        while d.isocalendar()[0] == year:
            d -= timedelta(days=1)
        year, week, _ = d.isocalendar()
    last_week_total, last_week_category_total = get_week_total(year, week)
    context.update({
        'entries': entries,
        'last_week_total': last_week_total,
        'last_week_category_total': last_week_category_total
    })
    return render(request, "spendtrackapp/summarize_week.html", context)
