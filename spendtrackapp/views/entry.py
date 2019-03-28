from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

from spendtrackapp.forms import EntryForm
from spendtrackapp.models import Entry
from spendtrackapp.views.utils import *


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
    entry_id = form.save().id

    return JsonResponse({'id': entry_id})


@login_required
def edit_handler(request):
    """Handle edit entry requests"""

    entry = get_entry(request)

    # return errors, if any
    if isinstance(entry, dict):
        return JsonResponse(entry, status=400)

    form = EntryForm(get_post(request), instance=entry)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)

    form.save()
    return JsonResponse({})


@login_required
def delete_handler(request):
    """Handle delete plan requests"""

    entry = get_entry(request)

    # return errors, if any
    if isinstance(entry, dict):
        return JsonResponse(entry, status=400)

    entry.delete()
    return JsonResponse({})


def get_entry(request):
    if 'id' not in request.POST:
        errors = 'Missing entry id'
    else:
        try:
            entry_id = int(request.POST['id'])
            entry = Entry.objects.get(id=entry_id)
            if entry.user_id != request.user.id:
                raise ValueError
            return entry
        except (Entry.DoesNotExist, ValueError):
            errors = 'Invalid entry id'

    return {'id': [errors]}
