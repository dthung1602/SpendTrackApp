from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

from spendtrackapp.forms import SearchTimeForm, PlanForm
from spendtrackapp.models import Plan
from spendtrackapp.views.utils import *


@login_required
def index_handler(request):
    """Handle plan index page"""

    return render(request, 'spendtrackapp/plan_index.html', {
        'categories': Category.objects.all(),
        'current_plans': Plan.get_current_plans(),
    })


@login_required
def search_handler(request):
    """Handle find plan requests"""

    # GET request -> render page
    if request.method == 'GET':
        return render(
            request,
            'spendtrackapp/plan_search.html',
            {'categories': Category.objects.all()}
        )

    # POST request -> return Plans info in JSON format

    # parse input
    form = SearchTimeForm(request.POST)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)

    search_type = form.cleaned_data['search_type']
    year = form.cleaned_data['year']
    month = form.cleaned_data['month']
    week = form.cleaned_data['week']
    start_date = form.cleaned_data['start_date']
    end_date = form.cleaned_data['end_date']

    # get plans in specified time
    if search_type == 'year':
        plans = Plan.get_plans_in_year(year)
    elif search_type == 'month':
        plans = Plan.get_plans_in_month(year, month)
    elif search_type == 'week':
        plans = Plan.get_plans_in_week(year, week)
    else:
        plans = Plan.get_plans_in_date_range(start_date, end_date)

    # turn plans to dictionaries
    plan_fields = ['id', 'name', 'start_date', 'end_date', 'category_name', 'planned_total', 'compare',
                   'is_completed', 'total', 'has_passed', 'target']
    plan_dicts = []
    for plan in plans:
        cat = plan.category
        d = {'category': '' if cat is None else str(cat.id)}
        for field in plan_fields:
            if field == 'category_name':
                d[field] = str(cat.name) if cat is not None else 'all categories'
            else:
                d[field] = str(getattr(plan, field))
        plan_dicts.append(d)

    # send plans using JSON
    return JsonResponse({'plans': plan_dicts})


@login_required
def add_handler(request):
    """Handle add new plan requests"""

    form = PlanForm(request.POST)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)

    plan = form.save()
    return JsonResponse({
        'id': plan.id,
        'total': plan.total
    })


@login_required
def edit_handler(request):
    """Handle edit plan requests"""

    # TODO prevent editing has_passed plans?

    plan = get_plan(request.POST)

    # return errors, if any
    if isinstance(plan, dict):
        return JsonResponse(plan, status=400)

    # noinspection PyUnboundLocalVariable
    form = PlanForm(request.POST, instance=plan)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)

    form.save()
    return JsonResponse({'total': plan.total})


@login_required
def delete_handler(request):
    """Handle delete plan requests"""

    plan = get_plan(request.POST)

    if isinstance(plan, dict):
        return JsonResponse(plan, status=400)

    plan.delete()
    return JsonResponse({})


def get_plan(data: dict):
    if 'id' not in data:
        errors = 'Missing plan'
    else:
        try:
            plan_id = int(data['id'])
            plan = Plan.objects.get(id=plan_id)
            return plan
        except (Plan.DoesNotExist, ValueError):
            errors = 'Invalid plan id'

    return {'id': [errors]}
