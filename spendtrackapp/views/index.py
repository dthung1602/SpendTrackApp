from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render

from spendtrackapp.forms import *
from spendtrackapp.models import *
from spendtrackapp.models import Category


@login_required
def index(request):
    """Handle home page get request"""

    current_balance = Info.get('CURRENT_BALANCE')
    root_categories = Category.get_root_categories()
    now = datetime.now()
    isoyear, week, week_day = now.isocalendar()
    entries_in_week = Entry.find_by_week(isoyear, week)
    total_in_week = Entry.total_by_week(isoyear, week)
    form = EntryForm()

    context = {
        'current_balance': current_balance,
        'root_categories': root_categories,
        'now': now,
        'entries_in_week': entries_in_week,
        'total_in_week': total_in_week,
        'form': form
    }
    return render(request, 'spendtrackapp/index.html', context)


@login_required
def add(request):
    """
    Handle add new entries request
    :return on success: an empty JSON object
            on failure: an JSON object whose properties' names are invalid fields
                        and whose values are list of errors in those fields
    """

    errors = {}

    # validate category_id
    if 'category_id' not in request.POST:
        errors.update({'category_id': ['Missing category']})
    else:
        category_id = request.POST['category_id']
        category = Category.get_leaf_category(category_id)
        if category is None:
            errors.update({'category_id': ['Invalid category']})

    # validate other fields
    form = EntryForm(request.POST)
    if not form.is_valid():
        errors.update(form.errors)

    # return errors, if any
    if errors:
        return JsonResponse(errors, status=400)

    # save
    entry = form.save()
    entry.change_category(category)
    entry.save()

    return JsonResponse({})
