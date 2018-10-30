from cgi import escape as escape_html

from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

from spendtrackapp.forms import *
from spendtrackapp.models import *
from spendtrackapp.views.utils import render


@login_required
def index_handler(request):
    """Handle home page get request"""

    current_balance = Info.get('CURRENT_BALANCE').value
    isoyear, week, week_day = datetime.now().isocalendar()
    entries_in_week = Entry.find_by_week(isoyear, week)
    total_in_week = Entry.total_by_week(isoyear, week)

    context = {
        'page_title': 'SpendTrackApp',
        'current_balance': current_balance,
        'category_hierarchy': category_hierarchy_html(),
        'entries_in_week': entries_in_week.all(),
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

    # save entry
    entry = form.save()
    # noinspection PyUnboundLocalVariable
    entry.change_category(category)
    entry.save()

    # change current balance
    current_balance = Info.get('CURRENT_BALANCE')
    current_balance += float(entry.value)
    current_balance.save()

    return JsonResponse({})


##############################################################
#                           UTILS                            #
##############################################################

def category_to_html(category: Category, level: int) -> str:
    """A recursive function return html of a category and all of its children"""

    # escape html
    category_name = escape_html(category.name)

    # base case: leaf category i.e. category has no children
    if category.is_leaf:
        return "<div class='category leaf' onclick='select({})'><div class='level-{}' id='cat-{}'>{}</div></div>" \
            .format(category.id, level, category.id, category_name)

    # recursively get html of its children
    sub_cat = "\n".join([category_to_html(sub_category, level + 1) for sub_category in category.children])

    return "<div class='category'><div class='level-{}'>{}</div></div>".format(level, category_name) + sub_cat


def category_hierarchy_html() -> str:
    """
    Return category hierarchy in html format

    E.g.
        - Cat 1
            - Cat 2      *
            - Cat 3
                -Cat 5   *
            - Cat 6      *
        - Cat 7          *

        * = leaf category

        <div class="category"><div class="level-1"> Cat 1 </div></div>
            <div class="category leaf"><div class="level-2"> Cat 2 </div></div>
            <div class="category"><div class="level-2"> Cat 3 </div></div>
                <div class="category leaf"><div class="level-3"> Cat 5 </div></div>
            <div class="category leaf"><div class="level-2"> Cat 6 </div></div>
        <div class="category leaf"><div class="level-1"> Cat 7 </div></div>
    """

    html_text = ""
    for root_category in Category.get_root_categories():
        html_text += category_to_html(root_category, 1)
    return html_text
