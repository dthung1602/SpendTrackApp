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
                'year': 2018
            },
            ['1', '2', '8', '9', '10', '11', '12', '5', '3', '6', '4', '7']
        ],
        [
            {
                'search_type': 'month',
                'year': 2019,
                'month': 1
            },
            ['1', '6', '7']
        ],
        [
            {
                'search_type': 'month',
                'year': 2018,
                'month': 11
            },
            ['1', '2', '8', '9', '10', '11', '12']
        ],
        [
            {
                'search_type': 'week',
                'year': 2018,
                'week': 48
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


def plan_test_add_success():
    return [
        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018-12-10',
                'end_date': '2018-12-10',
                'category': 3,
                'planned_total': 10.58,
                'compare': '<'
            },
            13
        ],
        [
            '2018-12-11',
            {
                'name': 'def',
                'start_date': '2018-12-15',
                'end_date': '2019-11-19',
                # 'category': None,
                'planned_total': 2.5,
                'compare': '>'
            },
            14
        ],
        [
            '2018-12-12',
            {
                'name': 'ghi',
                'start_date': '2018-12-12',
                'end_date': '2018-12-16',
                'category': 1,
                'planned_total': 1000000000.58,
                'compare': '='
            },
            15
        ],
    ]


def plan_test_add_fail():
    return [
        # missing, blank
        [
            '2018-12-10',
            {
                'start_date': '2018-12-10',
                'end_date': '2018-12-10',
                'category': 3,
                'planned_total': 10.58,
                'compare': '<'
            },
            ['name']
        ],
        [
            '2018-12-10',
            {
                'name': '',
                'start_date': '2018-12-10',
                'end_date': '2018-12-10',
                'category': 3,
                'planned_total': 10.58,
                'compare': '<'
            },
            ['name']
        ],

        [
            '2018-12-10',
            {
                'name': 'abc',
                'end_date': '2018-12-10',
                'category': 3,
                'planned_total': 10.58,
                'compare': '<'
            },
            ['start_date']
        ],
        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '',
                'end_date': '2018-12-10',
                'category': 3,
                'planned_total': 10.58,
                'compare': '<'
            },
            ['start_date']
        ],

        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018-12-10',
                'category': 3,
                'planned_total': 10.58,
                'compare': '<'
            },
            ['end_date']
        ],
        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018-12-10',
                'end_date': '',
                'category': 3,
                'planned_total': 10.58,
                'compare': '<'
            },
            ['end_date']
        ],

        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018-12-10',
                'end_date': '2018-12-10',
                'category': 3,
                'compare': '<'
            },
            ['planned_total']
        ],
        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018-12-10',
                'end_date': '2018-12-10',
                'category': 3,
                'planned_total': '',
                'compare': '<'
            },
            ['planned_total']
        ],

        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018-12-10',
                'end_date': '2018-12-10',
                'category': 3,
                'planned_total': 10.58,
            },
            ['compare']
        ],
        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018-12-10',
                'end_date': '2018-12-10',
                'category': 3,
                'planned_total': 10.58,
                'compare': ''
            },
            ['compare']
        ],

        # invalid date
        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '10000-12-10',
                'end_date': '0-12-10',
                'category': 3,
                'planned_total': 10.58,
                'compare': '='
            },
            ['start_date', 'end_date']
        ],
        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018/12/10',
                'end_date': '10-12-2019',
                'category': 3,
                'planned_total': 10.58,
                'compare': '='
            },
            ['start_date', 'end_date']
        ],
        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018-12-10',
                'end_date': '2017-12-10',
                'category': 3,
                'planned_total': 10.58,
                'compare': '='
            },
            ['end_date']
        ],
        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018-12-09',
                'end_date': '2019-12-10',
                'category': 3,
                'planned_total': 10.58,
                'compare': '='
            },
            ['start_date']
        ],

        # invalid category
        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018-12-10',
                'end_date': '2019-12-10',
                'category': 33,
                'planned_total': 10.58,
                'compare': '='
            },
            ['category']
        ],
        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018-12-10',
                'end_date': '2019-12-10',
                'category': 'abc',
                'planned_total': 10.58,
                'compare': '='
            },
            ['category']
        ],

        # invalid name
        [
            '2018-12-10',
            {
                'name': 'ab' * 25 + 'x',
                'start_date': '2018-12-10',
                'end_date': '2019-12-10',
                'category': 3,
                'planned_total': 10.58,
                'compare': '='
            },
            ['name']
        ],

        # invalid planned total
        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018-12-10',
                'end_date': '2019-12-10',
                'category': 3,
                'planned_total': 10.58999,
                'compare': '='
            },
            ['planned_total']
        ],
        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018-12-10',
                'end_date': '2019-12-10',
                'category': 3,
                'planned_total': -10.58,
                'compare': '='
            },
            ['planned_total']
        ],

        # compare
        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018-12-10',
                'end_date': '2019-12-10',
                'category': 3,
                'planned_total': 10.58,
                'compare': 'aa'
            },
            ['compare']
        ],
        [
            '2018-12-10',
            {
                'name': 'abc',
                'start_date': '2018-12-10',
                'end_date': '2019-12-10',
                'category': 3,
                'planned_total': 10.58,
                'compare': 'a'
            },
            ['compare']
        ],

        # Mixed
        [
            '2018-12-10',
            {
                'name': '',
                'start_date': '2018-12-100',
                'end_date': '20190-12-10',
                'category': 99,
                'planned_total': -10.58,
                'compare': 'a'
            },
            ['name', 'start_date', 'end_date', 'category', 'planned_total', 'compare']
        ],
    ]


def plan_test_edit_success():
    return [
        [
            '2018-12-10',
            {
                'id': 1,
                'name': 'abc',
                'start_date': '2018-12-10',
                'end_date': '2018-12-10',
                'category': 3,
                'planned_total': 10.58,
                'compare': '<'
            }
        ],
        [
            '2018-12-11',
            {
                'id': 2,
                'name': 'def',
                'start_date': '2018-12-15',
                'end_date': '2019-11-19',
                # 'category': None,
                'planned_total': 2.5,
                'compare': '>'
            }
        ],
        [
            '2018-12-12',
            {
                'id': '1',
                'name': 'ghi',
                'start_date': '2018-12-12',
                'end_date': '2018-12-16',
                'category': 1,
                'planned_total': 1000000000.58,
                'compare': '='
            }
        ],
    ]


def plan_test_edit_fail():
    data = plan_test_add_fail()
    for d in data:
        d[1]['id'] = 1
    data += [
        [
            '2018-12-12',
            {
                'name': 'ghi',
                'start_date': '2018-12-12',
                'end_date': '2018-12-16',
                'category': 1,
                'planned_total': 1000000000.58,
                'compare': '='
            },
            ['id']
        ],
        [
            '2018-12-12',
            {
                'id': '',
                'name': 'ghi',
                'start_date': '2018-12-12',
                'end_date': '2018-12-16',
                'category': 1,
                'planned_total': 1000000000.58,
                'compare': '='
            },
            ['id']
        ],
        [
            '2018-12-12',
            {
                'id': 'a',
                'name': 'ghi',
                'start_date': '2018-12-12',
                'end_date': '2018-12-16',
                'category': 1,
                'planned_total': 1000000000.58,
                'compare': '='
            },
            ['id']
        ],
        [
            '2018-12-12',
            {
                'id': 199,
                'name': 'ghi',
                'start_date': '2018-12-12',
                'end_date': '2018-12-16',
                'category': 1,
                'planned_total': 1000000000.58,
                'compare': '='
            },
            ['id']
        ]
    ]
    return data


def plan_test_delete_success():
    return [[{'id': i}] for i in range(1, 7)] + \
           [[{'id': str(i)}] for i in range(7, 13)]


def plan_test_delete_fail():
    return [
        [{'id': 0}],
        [{'id': 13}],
        [{'id': ''}],
        [{'id': 'a'}],
        [{'id': '0'}],
        [{'id': '13'}],
    ]
