from datetime import datetime
from math import inf as INF

from spendtrackapp.models import Info, Entry


def category_ancestors():
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


def category_children():
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


def category_is_leaf():
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


def category_get_leaf_category():
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


def category_get_root_categories():
    return [
        [[1, 10, 12]]
    ]


def entry_change_category_success():
    return [
        [1, 11, [11, 10]],
        [1, 13, [1, 3, 13]],
        [2, 8, [1, 2, 5, 8]],
        [2, 8, [1, 2, 5, 8]],
        [3, 12, [12]],
    ]


def entry_change_category_fail():
    return [
        [1, 1],
        [1, 2],
        [1, 3],
        [1, 5],
        [1, 10],
    ]


def entry_modify_date():
    return [
        [Entry._Entry__modify_start_date, 125, TypeError],
        [Entry._Entry__modify_start_date, 12.5, TypeError],
        [Entry._Entry__modify_start_date, True, TypeError],
        [Entry._Entry__modify_start_date, [], TypeError],
        [Entry._Entry__modify_start_date, '', ValueError],
        [Entry._Entry__modify_start_date, '2018 05 15', ValueError],
        [Entry._Entry__modify_start_date, '2018-05-15 15:15:15', ValueError],
        [Entry._Entry__modify_start_date, '2018-55-15', ValueError],
        [Entry._Entry__modify_start_date, '2018-05-99', ValueError],

        [Entry._Entry__modify_end_date, 125, TypeError],
        [Entry._Entry__modify_end_date, 12.5, TypeError],
        [Entry._Entry__modify_end_date, True, TypeError],
        [Entry._Entry__modify_end_date, [], TypeError],
        [Entry._Entry__modify_end_date, '', ValueError],
        [Entry._Entry__modify_end_date, '2018 05 15', ValueError],
        [Entry._Entry__modify_end_date, '2018-05-15 15:15:15', ValueError],
        [Entry._Entry__modify_end_date, '2018-55-15', ValueError],
        [Entry._Entry__modify_end_date, '2018-05-99', ValueError],
    ]


def entry_find_by_date_range():
    return [
        [None, None, [19, 7, 14, 16, 5, 21, 11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]],

        [datetime(2000, 1, 1), datetime(2020, 1, 1),
         [19, 7, 14, 16, 5, 21, 11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]],
        ['2000-1-1', '2020-1-1',
         [19, 7, 14, 16, 5, 21, 11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]],

        [None, datetime(2015, 11, 6), [19, 7, 14, 16]],
        [None, '2015-11-6', [19, 7, 14, 16]],
        [None, datetime(2017, 7, 1), [19, 7, 14, 16, 5, 21, 11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2]],
        [None, '2017-7-1', [19, 7, 14, 16, 5, 21, 11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2]],
        [datetime(2000, 1, 1), datetime(2017, 7, 1),
         [19, 7, 14, 16, 5, 21, 11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2]],
        ['2000-1-1', '2017-7-1', [19, 7, 14, 16, 5, 21, 11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2]],

        [datetime(2017, 8, 1), None, [1, 20, 18, 10, 8, 13, 26]],
        ['2017-8-1', None, [1, 20, 18, 10, 8, 13, 26]],
        [datetime(2017, 2, 6), None, [17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]],
        ['2017-2-6', None, [17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]],
        [datetime(2017, 2, 6), datetime(2020, 1, 1), [17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]],
        ['2017-2-6', '2020-1-1', [17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]],

        [datetime(2016, 1, 12), datetime(2017, 8, 11), [11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1]],
        ['2016-1-12', '2017-8-11', [11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1]],
        [datetime(2016, 1, 13), datetime(2017, 8, 11), [11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1]],
        ['2016-1-13', '2017-8-11', [11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1]],
        [datetime(2016, 1, 12), datetime(2017, 8, 10), [11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1]],
        ['2016-1-12', '2017-8-10', [11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1]],

        [datetime(2017, 12, 25), datetime(2018, 12, 31), []],
        ['2017-12-25', '2018-12-31', []]
    ]


def entry_find_by_year():
    return [
        [1000, []],
        [2013, []],
        [2014, [19, 7]],
        [2015, [14, 16, 5, 21]],
        [2016, [11, 4, 15, 3, 6]],
        [2017, [22, 23, 24, 25, 17, 9, 12, 2, 1, 20, 18, 10]],
        [2018, []],
        [2019, [8, 13, 26]],
        [2020, []],
        [9999, []],
    ]


def entry_find_by_month():
    return [
        [2014, 12, [19, 7]],
        [2015, 11, [16, 5, 21]],
        [2016, 1, [11, 4]],
        [2016, 1, [11, 4]],
        [2017, 10, [20, 18]],
        [2019, 2, [13]],

        [2019, 4, []],
        [2017, 4, []],
        [2000, 4, []],

        [1000, 1, []],
        [9999, 12, []],
    ]


def entry_find_by_week():
    return [
        [2014, 51, [19]],
        [2014, 52, [7]],
        [2015, 41, [14]],
        [2015, 45, [16, 5, 21]],
        [2016, 2, [11]],
        [2016, 4, [4]],
        [2016, 12, [15]],
        [2016, 27, [3]],
        [2016, 34, [6]],
        [2017, 6, [17]],
        [2017, 10, [9]],
        [2017, 24, [12]],
        [2017, 26, [2]],
        [2017, 32, [1]],
        [2017, 40, [20]],
        [2017, 41, [18]],
        [2017, 51, [10]],
        [2019, 1, [8]],
        [2019, 9, [13]],

        [2019, 52, []],
        [2020, 1, [26]],

        [2015, 1, []],
        [2019, 2, []],

        [1000, 1, []],
        [9999, 52, []],
    ]


def entry_total_by_date_range():
    return [
        [None, None, 189],

        [datetime(2000, 1, 1), datetime(2020, 1, 1), 189],
        ['2000-1-1', '2020-1-1', 189],

        [None, datetime(2015, 11, 6), 176],
        [None, '2015-11-6', 176],
        [None, datetime(2017, 7, 1), 93.5],
        [None, '2017-7-1', 93.5],
        [datetime(2000, 1, 1), datetime(2017, 7, 1), 93.5],
        ['2000-1-1', '2017-7-1', 93.5],

        [datetime(2017, 8, 1), None, 95.5],
        ['2017-8-1', None, 95.5],
        [datetime(2017, 2, 6), None, 33],
        ['2017-2-6', None, 33],
        [datetime(2017, 2, 6), datetime(2020, 1, 1), 33],
        ['2017-2-6', '2020-1-1', 33],

        [datetime(2016, 1, 12), datetime(2017, 8, 11), -21.5],
        ['2016-1-12', '2017-8-11', -21.5],
        [datetime(2016, 1, 13), datetime(2017, 8, 11), -21.5],
        ['2016-1-13', '2017-8-11', -21.5],
        [datetime(2016, 1, 12), datetime(2017, 8, 10), -21.5],
        ['2016-1-12', '2017-8-10', -21.5],

        [datetime(2017, 12, 25), datetime(2018, 12, 31), 0],
        ['2017-12-25', '2018-12-31', 0]
    ]


def entry_total_by_year():
    return [
        [1000, 0],
        [2013, 0],
        [2014, 76.5],
        [2015, 88.5],
        [2016, -28.5],
        [2017, 12.5],
        [2018, 0],
        [2019, 40],
        [2020, 0],
        [9999, 0],
    ]


def entry_total_by_month():
    return [
        [2014, 12, 75 + 1.5],
        [2015, 11, 100 - 8.5 - 2.5],
        [2016, 1, -8.5 - 1.5],
        [2017, 1, -1.5 - 1.5 + 25 - 2.5],
        [2017, 10, -12.5 - 2.5],
        [2019, 2, 50],

        [2019, 4, 0],
        [2017, 4, 0],
        [2000, 4, 0],

        [1000, 1, 0],
        [9999, 12, 0],
    ]


def entry_total_by_week():
    return [
        [2014, 51, 75],
        [2014, 52, 1.5],
        [2015, 41, -0.5],
        [2015, 45, 89],

        [2019, 52, 0],
        [2020, 1, -5],

        [2015, 1, 0],
        [2019, 2, 0],

        [1000, 1, 0],
        [9999, 52, 0],
    ]


def entry_find_by_date_range_with_category():
    return [
        [None, None, 'cat4', [14, 2, 1]],
        ['2018-12-29', '2019-12-31', 'cat2', []],
        ['2017-12-25', '2018-12-31', 'cat1', []],
        ['2016-1-12', '2017-8-11', 'cat7', [4, 3]]
    ]


def entry_find_by_year_with_category():
    return [
        [1000, 'cat9', []],
        [2013, 'cat2', []],
        [2014, 'cat10', [19]],
        [2016, 'cat5', [4, 15, 3, 6]],
        [2017, 'cat1', [2, 1]],
        [2017, 'cat100', []],
        [2018, 'cat2', []],
        [2020, 'cat2', []],
        [9999, 'cat2', []],
    ]


def entry_find_by_month_with_category():
    return [
        [2014, 12, 'cat1', [7]],
        [2015, 11, 'cat1', [16, 5]],
        [2016, 1, 'cat5', [4]],
        [2016, 1, 'cat99', []],

        [2019, 4, 'cat1', []],
        [2017, 4, 'cat1', []],
        [2000, 4, 'cat1', []],

        [1000, 1, 'cat1', []],
        [9999, 12, 'cat1', []],
    ]


def entry_find_by_week_with_category():
    return [
        [2015, 45, 'cat1', [16, 5]],
        [2015, 45, 'cat5', [16, 5]],
        [2015, 45, 'cat7', [5]],
        [2015, 45, 'cat2', []],
        [2015, 45, 'cat99', []],

        [2019, 52, 'cat12', []],
        [2020, 1, 'cat12', [26]],

        [2015, 1, 'cat1', []],
        [2019, 2, 'cat1', []],

        [1000, 1, 'cat1', []],
        [9999, 52, 'cat1', []],
    ]


def entry_find_by_date_range_with_limit():
    return [
        [None, None, INF,
         [19, 7, 14, 16, 5, 21, 11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]],
        [None, None, 27,
         [19, 7, 14, 16, 5, 21, 11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]],
        [None, None, 26,
         [19, 7, 14, 16, 5, 21, 11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1, 20, 18, 10, 8, 13, 26]],
        [None, None, 5, [19, 7, 14, 16, 5]],
        [None, None, 1, [19]],
        [None, None, 0, []],

        ['2016-1-12', '2017-8-11', INF, [11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1]],
        ['2016-1-12', '2017-8-11', 15, [11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1]],
        ['2016-1-12', '2017-8-11', 14, [11, 4, 15, 3, 6, 22, 23, 24, 25, 17, 9, 12, 2, 1]],
        ['2016-1-12', '2017-8-11', 5, [11, 4, 15, 3, 6]],
        ['2016-1-12', '2017-8-11', 1, [11]],
        ['2016-1-12', '2017-8-11', 0, []],

        ['2017-12-25', '2018-12-31', INF, []],
        ['2017-12-25', '2018-12-31', 5, []]
    ]


def entry_find_by_year_with_limit():
    return [
        [2013, INF, []],
        [2013, 5, []],

        [2014, INF, [19, 7]],
        [2014, 3, [19, 7]],
        [2014, 2, [19, 7]],
        [2014, 1, [19]],
        [2014, 0, []],

        [2017, INF, [22, 23, 24, 25, 17, 9, 12, 2, 1, 20, 18, 10]],
        [2017, 13, [22, 23, 24, 25, 17, 9, 12, 2, 1, 20, 18, 10]],
        [2017, 12, [22, 23, 24, 25, 17, 9, 12, 2, 1, 20, 18, 10]],
        [2017, 5, [22, 23, 24, 25, 17]],
        [2017, 2, [22, 23]],
        [2017, 1, [22]],
        [2017, 0, []],

        [2018, INF, []],
        [2018, 5, []],
    ]


def entry_find_by_month_with_limit():
    return [
        [2015, 11, INF, [16, 5, 21]],
        [2015, 11, 4, [16, 5, 21]],
        [2015, 11, 3, [16, 5, 21]],
        [2015, 11, 2, [16, 5]],
        [2015, 11, 1, [16]],
        [2015, 11, 0, []],

        [9999, 12, INF, []],
        [9999, 12, 5, []],
    ]


def entry_find_by_week_with_limit():
    return [
        [2015, 45, INF, [16, 5, 21]],
        [2015, 45, 4, [16, 5, 21]],
        [2015, 45, 3, [16, 5, 21]],
        [2015, 45, 1, [16]],
        [2015, 45, 0, []],

        [2019, 52, INF, []],
        [2019, 52, 5, []],

        [2020, 1, INF, [26]],
        [2020, 1, 2, [26]],
        [2020, 1, 1, [26]],
        [2020, 1, 0, []],
    ]


def info_get_success():
    return [
        ('a string', 'a long long long string', str),
        ('an int1', 58, int),
        ('an int2', -58, int),
        ('a float1', 58.1515, float),
        ('a float2', -58.1515, float),
        ('a float3', 58.1515e3, float),
        ('a bool1', True, bool),
        ('a bool2', True, bool),
        ('a bool3', False, bool),
        ('a bool4', False, bool)
    ]


def info_get_fail():
    return [
        ['does not exist', Info.DoesNotExist],
        [2, Info.DoesNotExist],
        [5.99, Info.DoesNotExist],

        ['fail int', ValueError],
        ['fail float', ValueError],
    ]


def info_set_success():
    return [
        ('a string', 'a new string'),
        ('an int1', 65),
        ('a float1', -1235.568),
        ('a bool1', True),
        ('a bool2', False),
    ]


def info_set_fail():
    return [
        ['does not exist', '', Info.DoesNotExist],
        [2, '', Info.DoesNotExist],
        [2.99, '', Info.DoesNotExist],

        ['an int1', 'abc', ValueError],
        ['an int1', 1.5, ValueError],
        ['a float1', 'abc', ValueError]
    ]
