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
