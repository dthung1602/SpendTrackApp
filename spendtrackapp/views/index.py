from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

from spendtrackapp.forms import EntryForm, Entry
from spendtrackapp.models import Info
from spendtrackapp.views.utils import *


@login_required
def index_handler(request):
    """Handle home page get request"""

    current_balance = Info.get('CURRENT_BALANCE').value
    isoyear, week, week_day = datetime.now().isocalendar()
    entries_in_week = group_array(Entry.find_by_week(isoyear, week), settings.VIEW_SUMMARIZE_WEEK_DEFAULT_PAGE_SIZE)
    total_in_week = Entry.total_by_week(isoyear, week)

    context = {
        'page_title': 'SpendTrackApp',
        'current_balance': current_balance,
        'category_hierarchy': category_hierarchy_html(),
        'entries_pages': entries_in_week,
        'total_in_week': total_in_week,
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

    form = EntryForm(request.POST)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)
    form.save()

    # change current balance
    current_balance = Info.get('CURRENT_BALANCE')
    current_balance += float(form.instance.value)
    current_balance.save()

    return JsonResponse({})
