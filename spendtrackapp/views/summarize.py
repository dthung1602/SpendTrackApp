from datetime import datetime, timedelta
from typing import Tuple, Dict

from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render

from spendtrackapp.models import Entry, Category


def get_date_range_total(start_date: str,
                         end_date: str) -> Tuple[float, Dict[str, float]]:
    """Get grand total and total of each category in the given date range"""

    total = float(Entry.total_by_date_range(start_date, end_date))
    category_total = {}
    for category in Category.objects.all():
        category_total[category.name] = float(
            Entry.total_by_date_range(start_date, end_date, category_name=category.name))
    return total, category_total


def get_year_total(year: int) -> Tuple[float, Dict[str, float]]:
    """Get grand total and total of each category in the given year"""

    total = float(Entry.total_by_year(year))
    category_total = {}
    for category in Category.objects.all():
        category_total[category.name] = float(Entry.total_by_year(year, category_name=category.name))
    return total, category_total


def get_month_total(year: int,
                    month: int) -> Tuple[float, Dict[str, float]]:
    """Get grand total and total of each category in the given month"""

    total = float(Entry.total_by_month(year, month))
    category_total = {}
    for category in Category.objects.all():
        category_total[category.name] = float(Entry.total_by_month(year, month, category_name=category.name))
    return total, category_total


def get_week_total(year: int,
                   week: int) -> Tuple[float, Dict[str, float]]:
    """Get grand total and total of each category in the given week"""

    total = float(Entry.total_by_week(year, week))
    category_total = {}
    for category in Category.objects.all():
        category_total[category.name] = float(Entry.total_by_week(year, week, category_name=category.name))
    return total, category_total


@login_required
def date_range_handler(request, start_date, end_date):
    """
    Handle summarize date range page
    If the request is AJAX, only grand total and total of each category in date range is returned in JSON format
    Otherwise, a full HTML document is returned
    """

    # AJAX request
    total, category_total = get_date_range_total(start_date, end_date)
    context = {
        'total': total,
        'category_total': category_total,
    }
    if request.is_ajax():
        return JsonResponse(context)

    # Ordinary request
    entries = list(Entry.find_by_date_range(start_date, end_date))
    context.update({
        'entries': entries
    })
    return render(request, "spendtrackapp/summarize_date_range.html", context)


@login_required
def year_handler(request, year):
    """
    Handle summarize year page
    If the request is AJAX, only grand total and total of each category in year is returned in JSON format
    Otherwise, a full HTML document is returned
    """

    # AJAX request
    this_year_total, this_year_category_total = get_year_total(year)
    context = {
        'this_year_total': this_year_total,
        'this_year_category_total': this_year_category_total,
    }
    if request.is_ajax():
        return JsonResponse(context)

    # Ordinary request
    entries = Entry.find_by_year(year)
    last_year_total, last_year_category_total = get_year_total(year - 1)
    context.update({
        'entries': entries,
        'last_year_total': last_year_total,
        'last_year_category_total': last_year_category_total
    })
    return render(request, "spendtrackapp/summarize_year.html", context)


@login_required
def month_handler(request, year, month):
    """
    Handle summarize month page
    If the request is AJAX, only grand total and total of each category in month is returned in JSON format
    Otherwise, a full HTML document is returned
    """

    # AJAX request
    this_month_total, this_month_category_total = get_month_total(year, month)
    context = {
        'this_month_total': this_month_total,
        'this_month_category_total': this_month_category_total,
    }
    if request.is_ajax():
        return JsonResponse(context)

    # Ordinary request
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
def week_handler(request, year, week):
    """
    Handle summarize week page
    If the request is AJAX, only grand total and total of each category in week is returned in JSON format
    Otherwise, a full HTML document is returned
    """

    # AJAX request
    this_week_total, this_week_category_total = get_week_total(year, week)
    context = {
        'this_week_total': this_week_total,
        'this_week_category_total': this_week_category_total,
    }
    if request.is_ajax():
        return JsonResponse(context)

    # Ordinary request
    entries = Entry.find_by_week(year, week)
    week -= 1
    if week == 0:  # get the last ISO week of last iso year
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
