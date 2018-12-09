def summarize_index_success():
    return [
        # all ok
        [
            {
                'summarize_type': 'year',
                'year_year': 2017
            },
            '/summarize/2017'
        ],
        [
            {
                'summarize_type': 'month',
                'month_year': 2015,
                'month_month': 'feb'
            },
            '/summarize/2015/feb'
        ],
        [
            {
                'summarize_type': 'month',
                'month_year': 2015,
                'month_month': 'FeB'
            },
            '/summarize/2015/feb'
        ],
        [
            {
                'summarize_type': 'week',
                'week_year': 2019,
                'week_week': 53
            },
            '/summarize/2019/w53'
        ],
        [
            {
                'summarize_type': 'daterange',
                'start_date': '2015-02-15',
                'end_date': '2015-12-03',
            },
            '/summarize/2015-02-15/2015-12-03'
        ],
    ]


def summarize_index_fail():
    return [
        # problems with summarize type
        [
            {
                'year_year': 2017
            },
            'Missing field'
        ],
        [
            {
                'summarize_type': 'abc',
                'year_year': 2017
            },
            'Invalid summarize type'
        ],

        # invalid fields
        [
            {
                'summarize_type': 'year',
                'year_year': 20179
            },
            'Invalid year'
        ],
        [
            {
                'summarize_type': 'month',
                'month_year': 20159,
                'month_month': 'feb'
            },
            'Invalid year or month'
        ],
        [
            {
                'summarize_type': 'month',
                'month_year': 2015,
                'month_month': 'xxx'
            },
            'Invalid year or month'
        ],
        [
            {
                'summarize_type': 'week',
                'week_year': 20199,
                'week_week': 52
            },
            'Invalid ISO year and week'
        ],
        [
            {
                'summarize_type': 'daterange',
                'start_date': '2015-99-15',
                'end_date': '2015-12-03',
            },
            'Invalid start date or end date'
        ],
        [
            {
                'summarize_type': 'daterange',
                'start_date': '2015-02-15',
                'end_date': '2015-12-32',
            },
            'Invalid start date or end date'
        ],
        [
            {
                'summarize_type': 'daterange',
                'start_date': '2015-12-15',
                'end_date': '2015-02-02',
            },
            'Invalid start date or end date'
        ],

        # missing fields
        [
            {
                'summarize_type': 'year',
            },
            'Missing field'
        ],
        [
            {
                'summarize_type': 'month',
                'month_month': 'feb'
            },
            'Missing field'
        ],
        [
            {
                'summarize_type': 'month',
                'month_year': 2015,
            },
            'Missing field'
        ],
        [
            {
                'summarize_type': 'week',
                'week_week': 53
            },
            'Missing field'
        ],
        [
            {
                'summarize_type': 'week',
                'week_year': 2019,
            },
            'Missing field'
        ],
        [
            {
                'summarize_type': 'daterange',
                'end_date': '2015-12-03',
            },
            'Missing field'
        ],
        [
            {
                'summarize_type': 'daterange',
                'start_date': '2015-02-15',
            },
            'Missing field'
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
