from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

from spendtrackapp.forms import EntryForm, Entry, Category
from spendtrackapp.views.utils import *


def index_handler(request):
    """Handle website index page"""

    context = {
        'page_title': 'SpendTrackApp',
        'user': None if request.user.is_anonymous else request.user
    }
    return render(request, 'spendtrackapp/index.html', context)


def legal_notice_handler(request):
    """
    Handle term and condition, privacy page
    """

    context = {
        'page_title': 'Legal notice | SpendTrackApp',
        'user': None if request.user.is_anonymous else request.user
    }
    return render(request, 'spendtrackapp/legal_notice.html', context)


def about_handler(request):
    """
    Handle about page
    """

    context = {
        'page_title': 'About | SpendTrackApp',
        'user': None if request.user.is_anonymous else request.user,
        'contact_dev_email': settings.CONTACT_DEV_EMAIL,
        'contact_dev_facebook': settings.CONTACT_DEV_FACEBOOK,
    }
    return render(request, 'spendtrackapp/about.html', context)


@login_required
def home_handler(request):
    """Handle user home page get request"""

    now = datetime.now()
    isoyear, week, week_day = now.isocalendar()
    year, month = now.year, now.month
    entries_in_week = group_array(
        Entry.find_by_week(request.user, isoyear, week), settings.VIEW_SUMMARIZE_WEEK_DEFAULT_PAGE_SIZE)
    total_in_week = Entry.total_by_week(request.user, isoyear, week)
    total_in_month = Entry.total_by_month(request.user, year, month)
    categories = Category.objects.all()

    context = {
        'page_title': 'Home | SpendTrackApp',
        'entries_pages': entries_in_week,
        'total_in_week': total_in_week,
        'total_in_month': total_in_month,
        'categories': categories
    }
    return render(request, 'spendtrackapp/home.html', context)


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
