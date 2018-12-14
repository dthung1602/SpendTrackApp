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


def index_add_success():
    return [
        [
            '2015-11-1',
            {'date': '2015-11-1', 'content': 'blah', 'value': 6, 'leaf_category': 6},
            [27],
            6,
        ],
        [
            '2015-11-2',
            {'date': '2015-11-2', 'content': 'blah', 'value': 16, 'leaf_category': 6},
            [16, 5, 21, 28],
            105,
        ],
        [
            '2015-11-8',
            {'date': '2015-11-8', 'content': 'blah', 'value': -9, 'leaf_category': 12},
            [16, 5, 21, 28, 29],
            96,
        ],
        [
            '2015-11-9',
            {'date': '2015-11-9', 'content': 'blah', 'value': 99, 'leaf_category': 11},
            [30],
            99,
        ],
    ]


def index_add_fail():
    return [
        [  # 0
            '2015-11-9',
            {'date': '2015-999-9', 'content': 'blah', 'value': 99, 'leaf_category': 11},
            ['date']
        ],
        [
            '2015-11-9',
            {'date': '2015-9-999', 'content': 'blah', 'value': 99, 'leaf_category': 11},
            ['date']
        ],
        [  # 2
            '2015-11-9',
            {'date': '2015-9-9 99:25:25', 'content': 'blah', 'value': 99, 'leaf_category': 11},
            ['date']
        ],
        [
            '2015-11-9',
            {'date': '2015-9-9 12:99:25', 'content': 'blah', 'value': 99, 'leaf_category': 11},
            ['date']
        ],
        [  # 4
            '2015-11-9',
            {'date': '2015-9-9 12:25:99', 'content': 'blah', 'value': 99, 'leaf_category': 11},
            ['date']
        ],
        [
            '2015-11-9',
            {'content': 'blah', 'value': 99, 'leaf_category': 11},
            ['date']
        ],

        [  # 6
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 'abc', 'leaf_category': 11},
            ['value']
        ],
        [
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'leaf_category': 11},
            ['value']
        ],

        [  # 8
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'leaf_category': 1},
            ['leaf_category']
        ],
        [
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'leaf_category': 2},
            ['leaf_category']
        ],
        [  # 10
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'leaf_category': 5},
            ['leaf_category']
        ],
        [
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'leaf_category': 99},
            ['leaf_category']
        ],
        [  # 12
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'leaf_category': 5.5},
            ['leaf_category']
        ],
        [
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'leaf_category': 'abc'},
            ['leaf_category']
        ],
        [  # 14
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99},
            ['leaf_category']
        ],
    ]
