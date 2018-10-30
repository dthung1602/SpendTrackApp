from django.conf import settings
from django.shortcuts import render as rd


def render(request, template_name, context=None, content_type=None, status=None, using=None):
    """Override render function to add information to context for base.html"""

    context['app_version'] = settings.APP_VERSION
    context['contact_email'] = settings.CONTACT_EMAIL
    context['contact_github'] = settings.CONTACT_GITHUB
    context['contact_facebook'] = settings.CONTACT_FACEBOOK

    return rd(request, template_name, context, content_type, status, using)
