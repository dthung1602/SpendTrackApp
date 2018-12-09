from django.http.response import HttpResponse

from spendtrackapp.models import Plan
from spendtrackapp.views.utils import render


def index(request):
    """Handle plan index page"""

    return render(request, "spendtrackapp/plan_index.html", {
        'current_plans': Plan.get_current_plans()
    })


def add(request):
    """Handle add new plan request"""

    return HttpResponse('add')


def delete(request):
    """Handle delete plan request"""

    return HttpResponse('del')


def edit(request):
    """Handle edit plan request"""

    return HttpResponse('edit')
