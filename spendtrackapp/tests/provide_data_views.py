def index_index_entries_in_week():
    return [
        ['2015-11-1', [], 0],
        ['2015-11-2', [16, 5, 21], 89],
        ['2015-11-6', [16, 5, 21], 89],
        ['2015-11-8', [16, 5, 21], 89],
        ['2015-11-9', [], 0],

        ['2019-12-29', [], 0],
        ['2019-12-30', [26], -5],
        ['2020-01-05', [26], -5],
        ['2020-01-06', [], 0],
    ]


def index_index_others():
    return [
        [152, [1, 10, 12]]
    ]


def index_add_success():
    return [
        [
            '2015-11-1',
            {'date': '2015-11-1', 'content': 'blah', 'value': 6, 'category_id': 6},
            [27],
            6,
        ],
        [
            '2015-11-2',
            {'date': '2015-11-2', 'content': 'blah', 'value': 16, 'category_id': 6},
            [16, 5, 21, 28],
            105,
        ],
        [
            '2015-11-8',
            {'date': '2015-11-8', 'content': 'blah', 'value': -9, 'category_id': 12},
            [16, 5, 21, 28, 29],
            96,
        ],
        [
            '2015-11-9',
            {'date': '2015-11-9', 'content': 'blah', 'value': 99, 'category_id': 11},
            [30],
            99,
        ],
    ]


def index_add_fail():
    return [
        [  # 0
            '2015-11-9',
            {'date': '2015-999-9', 'content': 'blah', 'value': 99, 'category_id': 11},
            ['date']
        ],
        [
            '2015-11-9',
            {'date': '2015-9-999', 'content': 'blah', 'value': 99, 'category_id': 11},
            ['date']
        ],
        [  # 2
            '2015-11-9',
            {'date': '2015-9-9 99:25:25', 'content': 'blah', 'value': 99, 'category_id': 11},
            ['date']
        ],
        [
            '2015-11-9',
            {'date': '2015-9-9 12:99:25', 'content': 'blah', 'value': 99, 'category_id': 11},
            ['date']
        ],
        [  # 4
            '2015-11-9',
            {'date': '2015-9-9 12:25:99', 'content': 'blah', 'value': 99, 'category_id': 11},
            ['date']
        ],
        [
            '2015-11-9',
            {'content': 'blah', 'value': 99, 'category_id': 11},
            ['date']
        ],

        [  # 6
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 'abc', 'category_id': 11},
            ['value']
        ],
        [
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'category_id': 11},
            ['value']
        ],

        [  # 8
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'category_id': 1},
            ['category_id']
        ],
        [
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'category_id': 2},
            ['category_id']
        ],
        [  # 10
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'category_id': 5},
            ['category_id']
        ],
        [
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'category_id': 99},
            ['category_id']
        ],
        [  # 12
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'category_id': 5.5},
            ['category_id']
        ],
        [
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'category_id': 'abc'},
            ['category_id']
        ],
        [  # 14
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99},
            ['category_id']
        ],
    ]


def summarize_date_range_ajax():
    return [
        # all
        ['2000-01-01', '2020-01-01', {
            'total': 189.00,
            'category_total': {
                'cat1': 114.50,
                'cat2': 46.50,
                'cat3': 0.00,
                'cat4': 46.50,
                'cat5': 68.00,
                'cat6': 0.00,
                'cat7': -12.00,
                'cat8': 85.00,
                'cat9': -5.00,
                'cat10': 42.50,
                'cat11': 80.50,
                'cat12': 32.00,
                'cat13': 0.00,
                'cat14': -38.00,
            }
        }],

        # [17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]
        ['2017-02-06', '2020-01-01', {
            'total': 33.0,
            'category_total': {
                'cat1': 42.00,
                'cat2': 47.00,
                'cat3': 0.00,
                'cat4': 47.00,
                'cat5': -5.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': -5.00,
                'cat10': -32.50,
                'cat11': 5.50,
                'cat12': 23.50,
                'cat13': 0.00,
                'cat14': -38.00,
            }
        }],

        ['2017-12-25', '2018-12-31', {
            'total': 0.00,
            'category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 0.00,
                'cat13': 0.00,
                'cat14': 0.00,
            }
        }]
    ]


def summarize_year_ajax():
    return [
        [2017, {
            'this_year_total': 12.50,
            'this_year_category_total': {
                'cat1': 47.00,
                'cat2': 47.00,
                'cat3': 0.00,
                'cat4': 47.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': -32.50,
                'cat11': 5.50,
                'cat12': -2.00,
                'cat13': 0.00,
                'cat14': -38.00,
            }
        }],

        [2016, {
            'this_year_total': -28.50,
            'this_year_category_total': {
                'cat1': -20.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': -20.00,
                'cat6': 0.00,
                'cat7': -3.50,
                'cat8': -16.50,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': -8.50,
                'cat13': 0.00,
                'cat14': 0.00,
            }
        }],

        [2018, {
            'this_year_total': 0.00,
            'this_year_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 0.00,
                'cat13': 0.00,
                'cat14': 0.00,
            }
        }]
    ]


def summarize_month_ajax():
    return [
        [2017, 1, {
            'this_month_total': 19.50,
            'this_month_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 19.50,
                'cat13': 0.00,
                'cat14': 0.00,
            }
        }],

        [2017, 10, {
            'this_month_total': -15.00,
            'this_month_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': -2.50,
                'cat11': 0.00,
                'cat12': -12.50,
                'cat13': 0.00,
                'cat14': -2.50,
            }
        }],

        [2017, 5, {
            'this_month_total': 0.00,
            'this_month_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 0.00,
                'cat13': 0.00,
                'cat14': 0.00,
            }
        }]
    ]


def summarize_week_ajax():
    return [
        [2015, 45, {
            'this_week_total': 89.00,
            'this_week_category_total': {
                'cat1': 91.50,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 91.50,
                'cat6': 0.00,
                'cat7': -8.50,
                'cat8': 100.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': -2.50,
                'cat13': 0.00,
                'cat14': 0.00,
            }
        }],

        [2019, 52, {
            'this_week_total': 0.00,
            'this_week_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 0.00,
                'cat13': 0.00,
                'cat14': 0.00,
            }
        }],

        [2020, 1, {
            'this_week_total': -5.00,
            'this_week_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': -5.00,
                'cat13': 0.00,
                'cat14': 0.00,
            }
        }]
    ]


def summarize_date_range():
    return [
        ['2000-01-01', '2020-01-01', {
            'total': 189.00,
            'category_total': {
                'cat1': 114.50,
                'cat2': 46.50,
                'cat3': 0.00,
                'cat4': 46.50,
                'cat5': 68.00,
                'cat6': 0.00,
                'cat7': -12.00,
                'cat8': 85.00,
                'cat9': -5.00,
                'cat10': 42.50,
                'cat11': 80.50,
                'cat12': 32.00,
                'cat13': 0.00,
                'cat14': -38.00,
            },
            'entries': [19, 7, 14, 16, 5, 21, 11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]
        }],

        ['2017-02-06', '2020-01-01', {
            'total': 33.0,
            'category_total': {
                'cat1': 42.00,
                'cat2': 47.00,
                'cat3': 0.00,
                'cat4': 47.00,
                'cat5': -5.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': -5.00,
                'cat10': -32.50,
                'cat11': 5.50,
                'cat12': 23.50,
                'cat13': 0.00,
                'cat14': -38.00,
            },
            'entries': [17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]
        }],

        ['2017-12-25', '2018-12-31', {
            'total': 0.00,
            'category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 0.00,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'entries': []
        }]
    ]


def summarize_year():
    return [
        [2016, {
            'this_year_total': -28.50,
            'this_year_category_total': {
                'cat1': -20.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': -20.00,
                'cat6': 0.00,
                'cat7': -3.50,
                'cat8': -16.50,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': -8.50,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'last_year_total': 88.5,
            'last_year_category_total': {
                'cat1': 91.00,
                'cat2': -0.50,
                'cat3': 0.00,
                'cat4': -0.50,
                'cat5': 91.50,
                'cat6': 0.00,
                'cat7': -8.50,
                'cat8': 100.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': -2.50,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'entries': [11, 4, 15, 3, 6]
        }],

        [2017, {
            'this_year_total': 12.50,
            'this_year_category_total': {
                'cat1': 47.00,
                'cat2': 47.00,
                'cat3': 0.00,
                'cat4': 47.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': -32.50,
                'cat11': 5.50,
                'cat12': -2.00,
                'cat13': 0.00,
                'cat14': -38.00,
            },
            'last_year_total': -28.50,
            'last_year_category_total': {
                'cat1': -20.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': -20.00,
                'cat6': 0.00,
                'cat7': -3.50,
                'cat8': -16.50,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': -8.50,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'entries': [22, 23, 24, 25, 17, 9, 12, 2, 1, 20, 18, 10]
        }],

        [2018, {
            'this_year_total': 0.00,
            'this_year_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 0.00,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'last_year_total': 12.50,
            'last_year_category_total': {
                'cat1': 47.00,
                'cat2': 47.00,
                'cat3': 0.00,
                'cat4': 47.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': -32.50,
                'cat11': 5.50,
                'cat12': -2.00,
                'cat13': 0.00,
                'cat14': -38.00,
            },
            'entries': []
        }]
    ]


def summarize_month():
    return [
        [2017, 1, {
            'this_month_total': 19.50,
            'this_month_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 19.50,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'last_month_total': 0.00,
            'last_month_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 0.00,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'entries': [22, 23, 24, 25]
        }],

        [2017, 10, {
            'this_month_total': -15.00,
            'this_month_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': -2.50,
                'cat11': 0.00,
                'cat12': -12.50,
                'cat13': 0.00,
                'cat14': -2.50,
            },
            'last_month_total': 0.00,
            'last_month_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 0.00,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'entries': [20, 18]
        }],

        [2017, 9, {
            'this_month_total': 0.00,
            'this_month_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 0.00,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'last_month_total': 50.00,
            'last_month_category_total': {
                'cat1': 50.00,
                'cat2': 50.00,
                'cat3': 0.00,
                'cat4': 50.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 0.00,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'entries': []
        }]
    ]


def summarize_week():
    return [
        [2017, 1, {
            'this_week_total': 21.00,
            'this_week_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 21.00,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'last_week_total': -1.50,
            'last_week_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': -1.50,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'entries': [23, 24, 25]
        }],

        [2019, 52, {
            'this_week_total': 0.00,
            'this_week_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 0.00,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'last_week_total': 0.00,
            'last_week_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 0.00,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'entries': []
        }],

        [2020, 1, {
            'this_week_total': -5.00,
            'this_week_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': -5.00,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'last_week_total': 0.00,
            'last_week_category_total': {
                'cat1': 0.00,
                'cat2': 0.00,
                'cat3': 0.00,
                'cat4': 0.00,
                'cat5': 0.00,
                'cat6': 0.00,
                'cat7': 0.00,
                'cat8': 0.00,
                'cat9': 0.00,
                'cat10': 0.00,
                'cat11': 0.00,
                'cat12': 0.00,
                'cat13': 0.00,
                'cat14': 0.00,
            },
            'entries': [26]
        }]
    ]
