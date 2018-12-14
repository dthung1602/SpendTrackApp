def summarize_index_success():
    return [
        # all ok
        [
            {
                'search_type': 'year',
                'year': 2017
            },
            '/summarize/2017'
        ],
        [
            {
                'search_type': 'month',
                'year': 2015,
                'month': 2
            },
            '/summarize/2015/feb'
        ],
        [
            {
                'search_type': 'month',
                'year': 2015,
                'month': '2'
            },
            '/summarize/2015/feb'
        ],
        [
            {
                'search_type': 'week',
                'year': 2019,
                'week': 53
            },
            '/summarize/2019/w53'
        ],
        [
            {
                'search_type': 'date_range',
                'start_date': '2015-02-15',
                'end_date': '2015-12-03',
            },
            '/summarize/2015-02-15/2015-12-03'
        ],
        # extra fields are sent
        [
            {
                'search_type': 'year',
                'year': 2017,
                'month': 5,
                'week': 6,
                'start_date': '2015-02-15',
                'end_date': '2015-12-03',
                'abc': 'xyz'
            },
            '/summarize/2017'
        ],
        [
            {
                'search_type': 'month',
                'year': 2015,
                'month': '2',
                'week': 52,
                'start_date': '2015-02-15',
                'end_date': '2015-12-03',
                'abc': 'xyz'
            },
            '/summarize/2015/feb'
        ],
        [
            {
                'search_type': 'week',
                'year': 2019,
                'week': 53,
                'month': '2',
                'start_date': '2015-02-15',
                'end_date': '2015-12-03',
                'abc': 'xyz'
            },
            '/summarize/2019/w53'
        ],
        [
            {
                'search_type': 'date_range',
                'start_date': '2015-02-15',
                'end_date': '2015-12-03',
                'year': 2019,
                'week': 53,
                'month': '2',
                'abc': 'xyz'
            },
            '/summarize/2015-02-15/2015-12-03'
        ],
    ]


def summarize_index_fail():
    return [
        # problems with search type
        [
            {
                'year': 2017
            },
            ['search_type']
        ],
        [
            {
                'search_type': 'abc',
                'year': 2017
            },
            ['search_type']
        ],

        # invalid year
        [
            {
                'search_type': 'year',
                'year': 20179
            },
            ['year']
        ],
        [
            {
                'search_type': 'year',
                'year': 179
            },
            ['year']
        ],
        [
            {
                'search_type': 'year',
                'year': 'abc'
            },
            ['year']
        ],

        # invalid month
        [
            {
                'search_type': 'month',
                'month': 2
            },
            ['year']
        ],
        [
            {
                'search_type': 'month',
                'year': 2015,
            },
            ['month']
        ],
        [
            {
                'search_type': 'month',
                'year': 2059,
                'month': 13
            },
            ['month']
        ],
        [
            {
                'search_type': 'month',
                'year': 2015,
                'month': 0
            },
            ['month']
        ],
        [
            {
                'search_type': 'month',
                'year': 2015,
                'month': 'abc'
            },
            ['month']
        ],

        # invalid week
        [
            {
                'search_type': 'week',
                'week': 52
            },
            ['year']
        ],
        [
            {
                'search_type': 'week',
                'year': 2019,
            },
            ['week']
        ],
        [
            {
                'search_type': 'week',
                'year': 2019,
                'week': 54
            },
            ['week']
        ],
        [
            {
                'search_type': 'week',
                'year': 2019,
                'week': 0
            },
            ['week']
        ],
        [
            {
                'search_type': 'week',
                'year': 2019,
                'week': 'abc'
            },
            ['week']
        ],

        # invalid date range
        [
            {
                'search_type': 'date_range',
                'start_date': '2015-99-15',
                'end_date': '2015-12-03',
            },
            ['start_date']
        ],
        [
            {
                'search_type': 'date_range',
                'start_date': '2015-02-15',
                'end_date': '2015-12-32',
            },
            ['end_date']
        ],
        [
            {
                'search_type': 'date_range',
                'start_date': '2015-12-15',
                'end_date': '2015-02-02',
            },
            ['end_date']
        ],
        [
            {
                'search_type': 'date_range',
                'end_date': '2015-12-03',
            },
            ['start_date']
        ],
        [
            {
                'search_type': 'date_range',
                'start_date': '2015-02-15',
            },
            ['end_date']
        ],

        # combine
        [
            {
                'search_type': 'date_range',
                'start_date': '2015-02-95',
            },
            ['start_date', 'end_date']
        ],
        [
            {
                'search_type': 'month',
                'year': 20015,
                'month': 16,
            },
            ['year', 'month']
        ],
        [
            {
                'search_type': 'week',
                'week': 55,
            },
            ['year', 'week']
        ],
    ]


def summarize_date_range_ajax():
    return [
        # all
        ['2000-01-01', '2020-01-01', {
            'total': 189,
            'category_total': [114.50, 42.50, 80.50, 32, 0, -38, 46.50, 0, 46.50, 68, 0, -12, 85, -5],
        }],

        # [17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]
        ['2017-02-06', '2020-01-01', {
            'total': 33.0,
            'category_total': [42, -32.50, 5.50, 23.50, 0, -38, 47, 0, 47, -5, 0, 0, 0, -5]
        }],

        ['2017-12-25', '2018-12-31', {
            'total': 0,
            'category_total': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }]
    ]


def summarize_year_ajax():
    return [
        [2017, {
            'total': 12.50,
            'category_total': [47, -32.50, 5.50, -2, 0, -38, 47, 0, 47, 0, 0, 0, 0, 0],
            'sub_period_total': [19.5, -35.5, -15, 0, 0, -9, -3, 50, 0, -15, 0, 20.5]
        }],

        [2016, {
            'total': -28.50,
            'category_total': [-20, 0, 0, -8.50, 0, 0, 0, 0, 0, -20, 0, -3.50, -16.50, 0],
            'sub_period_total': [-10, 0, -25.5, 0, 0, 0, -2, 9, 0, 0, 0, 0]
        }],

        [2018, {
            'total': 0,
            'category_total': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'sub_period_total': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }]
    ]


def summarize_month_ajax():
    return [
        [2017, 1, {
            'total': 19.50,
            'category_total': [0, 0, 0, 19.50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'sub_period_total': [
                -1.5, 0, 23.5, 0, -2.5, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ]
        }],

        [2017, 10, {
            'total': -15,
            'category_total': [0, -2.50, 0, -12.50, 0, -2.50, 0, 0, 0, 0, 0, 0, 0, 0],
            'sub_period_total': [
                0, -12.5, 0, 0, 0, 0, 0, 0, 0, 0,
                0, -2.5, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ]
        }],

        [2017, 5, {
            'total': 0,
            'category_total': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'sub_period_total': [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ]
        }]
    ]


def summarize_week_ajax():
    return [
        [2015, 45, {
            'total': 89,
            'category_total': [91.50, 0, 0, -2.50, 0, 0, 0, 0, 0, 91.50, 0, -8.50, 100, 0],
            'sub_period_total': [0, 0, 0, 100, 0, -11, 0]
        }],

        [2019, 52, {
            'total': 0,
            'category_total': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'sub_period_total': [0, 0, 0, 0, 0, 0, 0]
        }],

        [2020, 1, {
            'total': -5,
            'category_total': [0, 0, 0, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'sub_period_total': [0, -5, 0, 0, 0, 0, 0]
        }]
    ]


def summarize_date_range():
    return [
        ['2000-01-01', '2020-01-01', {
            'total': 189,
            'category_total': [114.50, 42.50, 80.50, 32, 0, -38, 46.50, 0, 46.50, 68, 0, -12, 85, -5],
            'entries': [19, 7, 14, 16, 5, 21, 11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]
        }],

        ['2017-02-06', '2020-01-01', {
            'total': 33.0,
            'category_total': [42, -32.50, 5.50, 23.50, 0, -38, 47, 0, 47, -5, 0, 0, 0, -5],
            'entries': [17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]
        }],

        ['2017-12-25', '2018-12-31', {
            'total': 0,
            'category_total': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'entries': []
        }]
    ]


def summarize_year():
    return [
        [2016, {
            'this_period_total': -28.50,
            'this_period_category_total': [-20, 0, 0, -8.50, 0, 0, 0, 0, 0, -20, 0, -3.50, -16.50, 0],
            'this_sub_period_total': [-10, 0, -25.5, 0, 0, 0, -2, 9, 0, 0, 0, 0],
            'last_period_total': 88.5,
            'last_period_category_total': [91, 0, 0, -2.50, 0, 0, -0.50, 0, -0.50, 91.50, 0, -8.50, 100, 0],
            'last_sub_period_total': [0, 0, 0, 0, 0, 0, 0, 0, 0, -0.5, 89, 0],
            'entries': [11, 4, 15, 3, 6]
        }],

        [2017, {
            'this_period_total': 12.50,
            'this_period_category_total': [47, -32.50, 5.50, -2, 0, -38, 47, 0, 47, 0, 0, 0, 0, 0],
            'this_sub_period_total': [19.5, -35.5, -15, 0, 0, -9, -3, 50, 0, -15, 0, 20.5],
            'last_period_total': -28.50,
            'last_period_category_total': [-20, 0, 0, -8.50, 0, 0, 0, 0, 0, -20, 0, -3.50, -16.50, 0],
            'last_sub_period_total': [-10, 0, -25.5, 0, 0, 0, -2, 9, 0, 0, 0, 0],
            'entries': [22, 23, 24, 25, 17, 9, 12, 2, 1, 20, 18, 10]
        }],

        [2018, {
            'this_period_total': 0,
            'this_period_category_total': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'this_sub_period_total': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'last_period_total': 12.50,
            'last_period_category_total': [47, -32.50, 5.50, -2, 0, -38, 47, 0, 47, 0, 0, 0, 0, 0],
            'last_sub_period_total': [19.5, -35.5, -15, 0, 0, -9, -3, 50, 0, -15, 0, 20.5],
            'entries': []
        }]
    ]


def summarize_month():
    return [
        [2017, 1, {
            'this_period_total': 19.50,
            'this_period_category_total': [0, 0, 0, 19.50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'this_sub_period_total': [
                -1.5, 0, 23.5, 0, -2.5, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ],
            'last_period_total': 0,
            'last_period_category_total': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'last_sub_period_total': [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ],
            'entries': [22, 23, 24, 25]
        }],

        [2017, 10, {
            'this_period_total': -15,
            'this_period_category_total': [0, -2.50, 0, -12.50, 0, -2.50, 0, 0, 0, 0, 0, 0, 0, 0],
            'this_sub_period_total': [
                0, -12.5, 0, 0, 0, 0, 0, 0, 0, 0,
                0, -2.5, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ],
            'last_period_total': 0,
            'last_period_category_total': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'last_sub_period_total': [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ],
            'entries': [20, 18]
        }],

        [2017, 9, {
            'this_period_total': 0,
            'this_period_category_total': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'this_sub_period_total': [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ],
            'last_period_total': 50,
            'last_period_category_total': [50, 0, 0, 0, 0, 0, 50, 0, 50, 0, 0, 0, 0, 0],
            'last_sub_period_total': [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 50,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ],
            'entries': []
        }]
    ]


def summarize_week():
    return [
        [2017, 1, {
            'this_period_total': 21,
            'this_period_category_total': [0, 0, 0, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'this_sub_period_total': [0, 23.5, 0, -2.5, 0, 0, 0],
            'last_period_total': -1.50,
            'last_period_category_total': [0, 0, 0, -1.50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'last_sub_period_total': [0, 0, 0, 0, 0, 0, -1.5],
            'entries': [23, 24, 25]
        }],

        [2019, 52, {
            'this_period_total': 0,
            'this_period_category_total': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'this_sub_period_total': [0, 0, 0, 0, 0, 0, 0],
            'last_period_total': 0,
            'last_period_category_total': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'last_sub_period_total': [0, 0, 0, 0, 0, 0, 0],
            'entries': []
        }],

        [2020, 1, {
            'this_period_total': -5,
            'this_period_category_total': [0, 0, 0, -5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'this_sub_period_total': [0, -5, 0, 0, 0, 0, 0],
            'last_period_total': 0,
            'last_period_category_total': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            'last_sub_period_total': [0, 0, 0, 0, 0, 0, 0],
            'entries': [26]
        }]
    ]
