from datetime import datetime, timedelta
from typing import Tuple, Dict

from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import reverse

from spendtrackapp.models import Entry, Category
from spendtrackapp.views.utils import render


@login_required
def index(request):
    """Handle index summarize page"""

    # GET request => render page
    if request.method == 'GET':
        return render(request, "spendtrackapp/summarize_index.html")

    # POST request => redirect

    if 'summarize_type' not in request.POST:
        return HttpResponseBadRequest('Missing field')
    summarize_type = request.POST['summarize_type']

    # year
    if summarize_type == 'year':
        if 'year_year' not in request.POST:
            return HttpResponseBadRequest('Missing field')
        year = request.POST['year_year']
        if not is_valid_year(year):
            return HttpResponseBadRequest('Invalid year')
        return HttpResponseRedirect(
            reverse('summarize:year', kwargs={'year': year})
        )

    # month
    if summarize_type == 'month':
        if 'month_month' not in request.POST \
                or 'month_year' not in request.POST:
            return HttpResponseBadRequest('Missing field')
        year = request.POST['month_year']
        month = request.POST['month_month']
        if not is_valid_year(year) or not is_valid_month(month):
            return HttpResponseBadRequest('Invalid year or month')
        return HttpResponseRedirect(
            reverse('summarize:month', kwargs={'year': year, 'month': month})
        )

    # week
    if summarize_type == 'week':
        if 'week_week' not in request.POST \
                or 'week_year' not in request.POST:
            return HttpResponseBadRequest('Missing field')
        year = request.POST['week_year']
        week = request.POST['week_week']
        if not is_valid_iso_week(year, week):
            return HttpResponseBadRequest('Invalid ISO year and week')
        return HttpResponseRedirect(
            reverse('summarize:week', kwargs={'year': year, 'week': week})
        )

    # date range
    if summarize_type == 'daterange':
        if 'start_date' not in request.POST \
                or 'end_date' not in request.POST:
            return HttpResponseBadRequest('Missing field')
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        if not is_valid_dates(start_date, end_date):
            return HttpResponseBadRequest('Invalid start date or end date')
        
        return HttpResponseRedirect(
            reverse('summarize:date_range', kwargs={'start_date': start_date, 'end_date': end_date})
        )

    # bad summarize-type
    return HttpResponseBadRequest('Invalid summarize type')


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
    entries = Entry.find_by_date_range(start_date, end_date)
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


@login_required
def this_year_handler(request):
    """Handle summarize this year page"""
    now = datetime.now()
    return year_handler(request, now.year)


@login_required
def this_month_handler(request):
    """Handle summarize this month page"""
    now = datetime.now()
    return month_handler(request, now.year, now.month)


@login_required
def this_week_handler(request):
    """Handle summarize this week page"""
    isoyear, week, _ = datetime.now().isocalendar()
    return week_handler(request, isoyear, week)


##############################################################
#                        UTILITIES                           #
##############################################################

def get_date_range_total(start_date: str,
                         end_date: str) -> Tuple[float, Dict[str, float]]:
    """Get grand total and total of each category in the given date range"""

    total = float(Entry.total_by_date_range(start_date, end_date))
    category_total = {}
    # todo inefficient
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


def is_valid_year(year: str) -> bool:
    """Check whether the given year is valid"""

    try:
        year = int(year)
        return 1000 <= year <= 9999
    except ValueError:
        return False


def is_valid_month(month: str) -> bool:
    """Check whether the given month is valid"""

    return month.lower() in [
        'jan', 'feb', 'mar', 'apr',
        'may', 'jun', 'jul', 'aug',
        'sep', 'oct', 'nov', 'dec'
    ]


def is_valid_iso_week(year: str, week: str) -> bool:
    """Check whether the given ISO week & ISO year is valid"""

    try:
        datetime.strptime(year + ' ' + week, '%Y %W')
        return True
    except ValueError:
        return False


def is_valid_dates(start_date: str, end_date: str) -> bool:
    """Check whether the given start_date and end_date are valid"""

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        return start_date <= end_date
    except ValueError:
        return False
