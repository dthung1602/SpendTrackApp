from spendtrackapp.tests.test_models.provide_data_test_plan import plan_get_current_plans
from spendtrackapp.tests.test_views.provide_data_test_summarize import summarize_index_fail


def plan_test_index():
    return plan_get_current_plans()


def plan_test_find_success():
    return [
        # all ok
        [
            {
                'search_type': 'year',
                'year_year': 2018
            },
            ['1', '2', '8', '9', '10', '11', '12', '5', '3', '6', '4', '7']
        ],
        [
            {
                'search_type': 'month',
                'month_year': 2019,
                'month_month': 'jan'
            },
            ['1', '6', '7']
        ],
        [
            {
                'search_type': 'month',
                'month_year': 2018,
                'month_month': 'NoV'
            },
            ['1', '2', '8', '9', '10', '11', '12']
        ],
        [
            {
                'search_type': 'week',
                'week_year': 2018,
                'week_week': 48
            },
            ['1', '2', '8', '9', '10', '11', '12']
        ],
        [
            {
                'search_type': 'date_range',
                'start_date': '2018-12-03',
                'end_date': '2018-12-03',
            },
            ['1', '8', '9', '10', '11', '12', '5', '3', '6']
        ],
    ]


def plan_test_find_fail():
    return summarize_index_fail()
