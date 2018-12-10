from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest, JsonResponse

from spendtrackapp.forms import PlanForm
from spendtrackapp.models import Plan
from spendtrackapp.views.utils import *


@login_required
def index_handler(request):
    """Handle plan index page"""

    return render(request, "spendtrackapp/plan_index.html", {
        'current_plans': Plan.get_current_plans(),
        'category_hierarchy': category_hierarchy_html(all_category=True),
    })


@login_required
def find_handler(request):
    """Handle find plan requests"""

    try:
        # parse input
        search_type, kwargs = get_search_date(request)

        # get plans in specified time
        get_plans_func = getattr(Plan, "get_plans_in_" + search_type)
        plans = get_plans_func(**kwargs)

        # turn plans to dictionaries
        plan_fields = ['id', 'name', 'start_date', 'end_date', 'category_name', 'planned_total', 'compare',
                       'is_completed', 'total', 'has_passed']
        plan_dicts = []
        for plan in plans:
            d = {}
            for field in plan_fields:
                if field == 'category_name':
                    d[field] = str(plan.category.name) if plan.category is not None else 'All categories'
                else:
                    d[field] = str(getattr(plan, field))
            plan_dicts.append(d)

        # send plans using JSON
        return JsonResponse({'plans': plan_dicts})

    except BadRequestException as e:
        return HttpResponseBadRequest(str(e))


@login_required
def add_handler(request):
    """Handle add new plan requests"""

    form = PlanForm(request.POST)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)

    plan = form.save()
    return JsonResponse({'id': plan.id})


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
    return JsonResponse({})


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
