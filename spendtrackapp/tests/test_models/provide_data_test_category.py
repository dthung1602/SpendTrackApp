
def ancestors():
    return [
        [1, []],
        [2, [1]],
        [3, [1]],
        [4, [1, 2]],
        [5, [1, 2]],
        [6, [1, 3]],
        [7, [1, 2, 5]],
        [8, [1, 2, 5]],
        [9, [1, 2, 5]],
        [10, []],
        [11, [10]],
        [12, []],
        [13, [1, 3]],
        [14, [10]]
    ]


def children():
    return [
        [1, [2, 3]],
        [2, [4, 5]],
        [3, [6, 13]],
        [4, []],
        [5, [7, 8, 9]],
        [6, []],
        [7, []],
        [8, []],
        [9, []],
        [10, [11, 14]],
        [11, []],
        [12, []],
        [13, []],
        [14, []]
    ]


def is_leaf():
    return [
        [1, False],
        [2, False],
        [3, False],
        [4, True],
        [5, False],
        [6, True],
        [7, True],
        [8, True],
        [9, True],
        [10, False],
        [11, True],
        [12, True],
        [13, True],
        [14, True]
    ]


def get_leaf_category():
    return [
        [1, False],
        [2, False],
        [3, False],
        [4, True],
        [5, False],
        [6, True],
        [7, True],
        [8, True],
        [9, True],
        [10, False],
        [11, True],
        [12, True],
        [13, True],
        [14, True],

        [0, False],
        [99, False],
        [1.158, False],
        ['abc', False]
    ]


def get_root_categories():
    return [
        [[1, 10, 12]]
    ]
