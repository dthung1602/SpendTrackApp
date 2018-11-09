from django.conf import settings
from django.shortcuts import render as rd
from datetime import datetime
from math import ceil

month_full_names = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


def render(request, template_name, context=None, content_type=None, status=None, using=None):
    """Override render function to add information to context for base.html"""

    if context is None:
        context = {}
    context['now'] = datetime.now()
    context['app_version'] = settings.APP_VERSION
    context['contact_email'] = settings.CONTACT_EMAIL
    context['contact_github'] = settings.CONTACT_GITHUB
    context['contact_facebook'] = settings.CONTACT_FACEBOOK

    return rd(request, template_name, context, content_type, status, using)


def group_array(arr, group_size):
    """Divide arr into groups with size at least group_size"""

    arr = list(arr)
    if group_size > 0:
        return [arr[i * group_size:i * group_size + group_size] for i in range(ceil(len(arr) / group_size))]
    return [arr]


def arr_to_js_str(arr, converter):
    """Convert a python array to a string represent Javascript array"""

    result = str([converter(i) for i in arr])
    if converter is bool:
        return result.replace('T', 't').replace('F', 'f')
    return result
