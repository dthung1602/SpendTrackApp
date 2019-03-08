from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

from spendtrackapp.forms import EntryForm, Entry, Category
from spendtrackapp.views.utils import *


@login_required
def index_handler(request):
    """Handle home page get request"""

    now = datetime.now()
    isoyear, week, week_day = now.isocalendar()
    year, month = now.year, now.month
    entries_in_week = group_array(
        Entry.find_by_week(request.user, isoyear, week), settings.VIEW_SUMMARIZE_WEEK_DEFAULT_PAGE_SIZE)
    total_in_week = Entry.total_by_week(request.user, isoyear, week)
    total_in_month = Entry.total_by_month(request.user, year, month)
    categories = Category.objects.all()

    context = {
        'page_title': 'SpendTrackApp',
        'entries_pages': entries_in_week,
        'total_in_week': total_in_week,
        'total_in_month': total_in_month,
        'categories': categories
    }
    return render(request, 'spendtrackapp/index.html', context)


@login_required
def add_handler(request):
    """
    Handle add new entries request
    :return on success: an empty JSON object
            on failure: an JSON object whose properties' names are invalid fields
                        and whose values are list of errors in those fields
    """

    form = EntryForm(get_post(request))
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    form.save()

    return JsonResponse({})


def legal_notice_handler(request):
    """
    Handle term and condition, privacy page
    """

    return render(request, 'spendtrackapp/legal_notice.html', {"page_title": "Legal notice"})
