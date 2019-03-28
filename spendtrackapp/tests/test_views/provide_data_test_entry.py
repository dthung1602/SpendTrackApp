def entry_add_success():
    return [
        [
            '2015-11-1',
            {'date': '2015-11-1', 'content': 'blah', 'value': 6, 'leaf_category': 6},
            [29],
            6,
        ],
        [
            '2015-11-2',
            {'date': '2015-11-2', 'content': 'blah', 'value': 16, 'leaf_category': 6},
            [16, 5, 21, 30],
            105,
        ],
        [
            '2015-11-8',
            {'date': '2015-11-8', 'content': 'blah', 'value': -9, 'leaf_category': 12},
            [16, 5, 21, 30, 31],
            96,
        ],
        [
            '2015-11-9',
            {'date': '2015-11-9', 'content': 'blah', 'value': 99, 'leaf_category': 11},
            [32],
            99,
        ],
    ]


def entry_add_fail():
    return [
        [  # 0
            '2015-11-9',
            {'date': '2015-999-9', 'content': 'blah', 'value': 99, 'leaf_category': 11},
            {'date'}
        ],
        [
            '2015-11-9',
            {'date': '2015-9-999', 'content': 'blah', 'value': 99, 'leaf_category': 11},
            {'date'}
        ],
        [  # 2
            '2015-11-9',
            {'date': '2015-9-9 99:25:25', 'content': 'blah', 'value': 99, 'leaf_category': 11},
            {'date'}
        ],
        [
            '2015-11-9',
            {'date': '2015-9-9 12:99:25', 'content': 'blah', 'value': 99, 'leaf_category': 11},
            {'date'}
        ],
        [  # 4
            '2015-11-9',
            {'date': '2015-9-9 12:25:99', 'content': 'blah', 'value': 99, 'leaf_category': 11},
            {'date'}
        ],
        [
            '2015-11-9',
            {'content': 'blah', 'value': 99, 'leaf_category': 11},
            {'date'}
        ],

        [  # 6
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 'abc', 'leaf_category': 11},
            {'value'}
        ],
        [
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'leaf_category': 11},
            {'value'}
        ],

        [  # 8
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'leaf_category': 1},
            {'leaf_category'}
        ],
        [
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'leaf_category': 2},
            {'leaf_category'}
        ],
        [  # 10
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'leaf_category': 5},
            {'leaf_category'}
        ],
        [
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'leaf_category': 99},
            {'leaf_category'}
        ],
        [  # 12
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'leaf_category': 5.5},
            {'leaf_category'}
        ],
        [
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99, 'leaf_category': 'abc'},
            {'leaf_category'}
        ],
        [  # 14
            '2015-11-9',
            {'date': '2015-9-9', 'content': 'blah', 'value': 99},
            {'leaf_category'}
        ],
    ]


def entry_edit_success():
    return [
        [{
            'id': 1,
            'date': '2019-05-03 20:15:30',
            'content': 'new content',
            'value': 78,
            'leaf_category': 7
        }],
        [{
            'id': 2,
            'date': '1999-05-03 02:15:00',
            'content': '<h1>new content</h1>',
            'value': 78.15,
            'leaf_category': 12
        }],
        [{
            'id': 1,
            'date': '2000-02-29 20:15:30',
            'content': 'x__',
            'value': -95,
            'leaf_category': 14
        }],
    ]


def entry_edit_fail():
    return [
        [
            {
                'date': '2019-05-03 20:15:30',
                'content': 'new content',
                'value': 78,
                'leaf_category': 7
            },
            {'id'}
        ],
        [
            {
                'id': 96,  # not exist
                'date': '2019-05-03 20:15:30',
                'content': 'new content',
                'value': 78,
                'leaf_category': 7
            },
            {'id'}
        ],
        [
            {
                'id': 28,  # belong to user 2
                'date': '2019-05-03 20:15:30',
                'content': 'new content',
                'value': 78,
                'leaf_category': 7
            },
            {'id'}
        ],

        [
            {
                'id': 1,
                'content': 'new content',
                'value': 78,
                'leaf_category': 7
            },
            {'date'}
        ],
        [
            {
                'id': 1,
                'date': '2019-13-03 20:15:30',
                'content': 'new content',
                'value': 78,
                'leaf_category': 7
            },
            {'date'}
        ],
        [
            {
                'id': 1,
                'date': '2019-05-03 25:15:30',
                'content': 'new content',
                'value': 78,
                'leaf_category': 7
            },
            {'date'}
        ],

        [
            {
                'id': 1,
                'date': '2019-05-03 20:15:30',
                'value': 78,
                'leaf_category': 7
            },
            {'content'}
        ],
        [
            {
                'id': 1,
                'date': '2019-05-03 20:15:30',
                'content': '',
                'value': 78,
                'leaf_category': 7
            },
            {'content'}
        ],
        [
            {
                'id': 1,
                'date': '2019-05-03 20:15:30',
                'content': 'new content' * 200,
                'value': 78,
                'leaf_category': 7
            },
            {'content'}
        ],

        [
            {
                'id': 1,
                'date': '2019-05-03 20:15:30',
                'content': 'new content',
                'leaf_category': 7
            },
            {'value'}
        ],
        [
            {
                'id': 1,
                'date': '2019-05-03 20:15:30',
                'content': 'new content',
                'value': 78.6565,
                'leaf_category': 7
            },
            {'value'}
        ],
        [
            {
                'id': 1,
                'date': '2019-05-03 20:15:30',
                'content': 'new content',
                'value': 'abc',
                'leaf_category': 7
            },
            {'value'}
        ],

        [
            {
                'id': 1,
                'date': '2019-05-03 20:15:30',
                'content': 'new content',
                'value': 78.23,
            },
            {'leaf_category'}
        ],

        [
            {
                'id': 1,
                'date': '2019-05-03 20:15:30',
                'content': 'new content',
                'value': 78.23,
                'leaf_category': 1  # not leaf
            },
            {'leaf_category'}
        ],
        [
            {
                'id': 1,
                'date': '2019-05-03 20:15:30',
                'content': 'new content',
                'value': 78.23,
                'leaf_category': 60  # not exist
            },
            {'leaf_category'}
        ],
        [
            {
                'id': 1,
                'date': '2019-05-03 20:15:30',
                'content': 'new content',
                'value': 78.23,
                'leaf_category': 'abc'
            },
            {'leaf_category'}
        ],

        [
            {
                'id': 1,
                'date': '2019-05-90 20:15:30',
                'content': '',
                'value': 78.263,
                'leaf_category': 1
            },
            {'leaf_category', 'value', 'content', 'date'}
        ],
    ]


def entry_delete_success():
    return [[i] for i in range(1, 27)]


def entry_delete_fail():
    return [[27], [28], [29], [0], ['abc']]
