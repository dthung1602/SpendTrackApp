from datetime import timedelta
from typing import Tuple, List

from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import reverse

from spendtrackapp.models import Entry, Category
from spendtrackapp.views.utils import *

categories = Category.objects.all().order_by('name')


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
    Handle summarize daterange page
    AJAX request: JSON format
    GET request: html format
    """

    # AJAX request
    date_range_info = get_date_range_info(start_date, end_date)
    context = {
        'total': date_range_info[0],
        'category_total': date_range_info[1],
        'daily_total': date_range_info[2],
    }
    if request.is_ajax():
        return JsonResponse(context)

    # GET request
    str_start_date = start_date.strftime('%Y-%m-%d')
    str_end_date = end_date.strftime('%Y-%m-%d')
    context = {
        'page_title': "From " + str_start_date + " to " + str_end_date,
        'categories_names': arr_to_js_str([category.name for category in categories], str),
        'is_leaf': arr_to_js_str([category.is_leaf for category in categories], bool),
        'start_date': str_start_date,
        'end_date': str_end_date,
        'total': date_range_info[0],
        'category_total': arr_to_js_str(date_range_info[1], float),
        'daily_total': arr_to_js_str(date_range_info[2], float),
        'entries_pages': date_range_info[3]
    }
    return render(request, "spendtrackapp/summarize_date_range.html", context)


@login_required
def year_handler(request, year):
    """
    Handle summarize year page
    AJAX request: only info of year is returned in JSON format
    GET request: info of year and the year before is returned
    """

    # AJAX request
    this_year = get_year_info(year)
    context = {
        'this_year_total': this_year[0],
        'this_year_category_total': this_year[1],
        'this_year_monthly_total': this_year[2]
    }
    if request.is_ajax():
        return JsonResponse(context)

    # GET request
    links = get_year_links(year)
    last_year = get_year_info(year - 1)

    context = {
        'page_title': year,
        'categories_names': arr_to_js_str([category.name for category in categories], str),
        'is_leaf': arr_to_js_str([category.is_leaf for category in categories], bool),

        'last_year_link': links[0],
        'last_year_name': links[1],
        'next_year_link': links[2],
        'next_year_name': links[3],

        'this_year_total': this_year[0],
        'this_year_category_total': arr_to_js_str(this_year[1], float),
        'this_year_monthly_total': arr_to_js_str(this_year[2], float),
        'entries_pages': this_year[3],

        'last_year_total': last_year[0],
        'last_year_category_total': arr_to_js_str(last_year[1], float),
        'last_year_monthly_total': arr_to_js_str(last_year[2], float),
    }
    return render(request, "spendtrackapp/summarize_year.html", context)


@login_required
def month_handler(request, year, month):
    """
    Handle summarize month page
    AJAX request: only info of month is returned in JSON format
    GET request: info of month and the month before is returned
    """

    # AJAX request
    this_month = get_month_info(year, month)
    context = {
        'this_month_total': this_month[0],
        'this_month_category_total': this_month[1],
        'this_month_daily_total': this_month[2]
    }
    if request.is_ajax():
        return JsonResponse(context)

    # GET request
    if month == 1:
        last_month = get_month_info(year - 1, 12)
    else:
        last_month = get_month_info(year, month - 1)

    links = get_month_links(year, month)

    context = {
        'page_title': month_full_names[month - 1] + " " + str(year),
        'categories_names': arr_to_js_str([category.name for category in categories], str),
        'is_leaf': arr_to_js_str([category.is_leaf for category in categories], bool),

        'last_month_link': links[0],
        'last_month_name': links[1],
        'next_month_link': links[2],
        'next_month_name': links[3],

        'this_month_total': this_month[0],
        'this_month_category_total': arr_to_js_str(this_month[1], float),
        'this_month_daily_total': arr_to_js_str(this_month[2], float),
        'entries_pages': this_month[3],

        'last_month_total': last_month[0],
        'last_month_category_total': arr_to_js_str(last_month[1], float),
        'last_month_daily_total': arr_to_js_str(last_month[2], float),
    }
    return render(request, "spendtrackapp/summarize_month.html", context)


@login_required
def week_handler(request, year, week):
    """
    Handle summarize week page
    AJAX request: only info of week is returned in JSON format
    GET request: info of week and the week before is returned
    """

    # AJAX request
    this_week = get_week_info(year, week)
    context = {
        'this_week_total': this_week[0],
        'this_week_category_total': this_week[1],
        'this_week_daily_total': this_week[2]
    }
    if request.is_ajax():
        return JsonResponse(context)

    # GET request
    prev_week = isoparse("%iW%02i" % (year, week)) - timedelta(days=7)
    prev_iso_year, prev_iso_week, _ = prev_week.isocalendar()
    last_week = get_week_info(prev_iso_year, prev_iso_week)

    links = get_week_links(year, week)

    context = {
        'page_title': str(year) + " week " + str(week),
        'categories_names': arr_to_js_str([category.name for category in categories], str),
        'is_leaf': arr_to_js_str([category.is_leaf for category in categories], bool),

        'last_week_link': links[0],
        'last_week_name': links[1],
        'next_week_link': links[2],
        'next_week_name': links[3],

        'this_week_total': this_week[0],
        'this_week_category_total': arr_to_js_str(this_week[1], float),
        'this_week_daily_total': arr_to_js_str(this_week[2], float),
        'entries_pages': this_week[3],

        'last_week_total': last_week[0],
        'last_week_category_total': arr_to_js_str(last_week[1], float),
        'last_week_daily_total': arr_to_js_str(last_week[2], float),
    }
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

def same_date(date1: datetime, date2: datetime) -> bool:
    """Check whether two given datetime object are in the same date"""

    return date1.day == date2.day and date1.month == date2.month and date1.year == date2.year


def get_date_range_info(start_date: str,
                        end_date: str) -> Tuple[float, List[float], List[float], List[List[Entry]]]:
    """Get grand total and total of each category in the given date range"""

    entries = list(Entry.find_by_date_range(start_date, end_date))
    total = sum([entry.value for entry in entries])
    total_by_category = [Entry.total_by_date_range(start_date, end_date, category_name=cat.name) for cat in categories]
    total_by_day = [sum([entry.value for entry in entries if same_date(entry.date, d)])
                    for d in daterange(start_date, end_date)]
    entries_pages = group_array(entries, settings.VIEW_SUMMARIZE_DATE_RANGE_DEFAULT_PAGE_SIZE)
    return total, total_by_category, total_by_day, entries_pages


def get_year_info(year: int) -> Tuple[float, List[float], List[float], List[List[Entry]]]:
    """Get grand total, total of each category, total of each month and entries (group into pages) in the given year"""

    entries = list(Entry.find_by_year(year))
    total = sum([entry.value for entry in entries])
    total_by_category = [Entry.total_by_year(year, category_name=cat.name) for cat in categories]
    total_by_month = [sum([entry.value for entry in entries if entry.date.month == m]) for m in range(1, 13)]
    entries_pages = group_array(entries, settings.VIEW_SUMMARIZE_YEAR_DEFAULT_PAGE_SIZE)
    return total, total_by_category, total_by_month, entries_pages


def get_month_info(year: int,
                   month: int) -> Tuple[float, List[float], List[float], List[List[Entry]]]:
    """Get grand total, total of each category, total of each month and entries (group into pages) in the given month"""

    entries = list(Entry.find_by_month(year, month))
    total = sum([entry.value for entry in entries])
    total_by_category = [Entry.total_by_month(year, month, category_name=cat.name) for cat in categories]
    total_by_day = [sum([entry.value for entry in entries if entry.date.day == d]) for d in range(1, 32)]
    entries_pages = group_array(entries, settings.VIEW_SUMMARIZE_MONTH_DEFAULT_PAGE_SIZE)
    return total, total_by_category, total_by_day, entries_pages


def get_week_info(year: int,
                  week: int) -> Tuple[float, List[float], List[float], List[List[Entry]]]:
    """Get grand total, total of each category, total of each month and entries (group into pages) in the given month"""

    entries = list(Entry.find_by_week(year, week))
    total = sum([entry.value for entry in entries])
    total_by_category = [Entry.total_by_week(year, week, category_name=cat.name) for cat in categories]
    monday = isoparse("%iW%02i" % (year, week))
    total_by_weekday = [sum([entry.value for entry in entries if same_date(entry.date, d)])
                        for d in daterange(monday, monday + timedelta(days=6))]
    entries_pages = group_array(entries, settings.VIEW_SUMMARIZE_WEEK_DEFAULT_PAGE_SIZE)
    return total, total_by_category, total_by_weekday, entries_pages


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
        isoparse("%iW%02i" % (int(year), int(week)))
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


def get_year_links(year):
    return [
        reverse("summarize:year", kwargs={'year': year - 1}),
        str(year - 1),
        reverse("summarize:year", kwargs={'year': year + 1}),
        str(year + 1)
    ]


def get_month_links(year, month):
    prev_year = year
    prev_month = month - 1
    if prev_month == 0:
        prev_month = 12
        prev_year = year - 1

    next_year = year
    next_month = month + 1
    if next_month == 13:
        next_month = 1
        next_year = year + 1

    prv = datetime(prev_year, prev_month, 1)
    nxt = datetime(next_year, next_month, 1)

    return [
        reverse("summarize:month", kwargs={'year': prv.year, 'month': prv.month}),
        prv.strftime("%B %Y"),
        reverse("summarize:month", kwargs={'year': nxt.year, 'month': nxt.month}),
        nxt.strftime("%B %Y"),
    ]


def get_week_links(year, week):
    s = "%iW%02i" % (year, week)
    this_week = isoparse(s)
    delta = timedelta(days=7)
    prev_week = this_week - delta
    next_week = this_week + delta
    prev_iso_year, prev_iso_week, _ = prev_week.isocalendar()
    next_iso_year, next_iso_week, _ = next_week.isocalendar()

    return [
        reverse("summarize:week", kwargs={'year': prev_iso_year, 'week': prev_iso_week}),
        str(prev_iso_year) + " week " + str(prev_iso_week),
        reverse("summarize:week", kwargs={'year': next_iso_year, 'week': next_iso_week}),
        str(next_iso_year) + " week " + str(next_iso_week)
    ]
