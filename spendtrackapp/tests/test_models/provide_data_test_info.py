from spendtrackapp.models import Info


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


def info_add_built_in_type():
    return [
        ['FLOAT1', 1.5, 3],
        ['FLOAT1', -0.5, 1],
        ['FLOAT1', 5, 6.5],
        ['FLOAT1', -3, -1.5],

        ['INT1', 1.5, 3.5],
        ['INT1', -0.5, 1.5],
        ['INT1', 5, 7],
        ['INT1', -3, -1],

        ['BOOL1', 1.5, 2.5],
        ['BOOL1', -0.5, 0.5],
        ['BOOL1', 5, 6],
        ['BOOL1', -3, -2],

        ['BOOL2', 1.5, 1.5],
        ['BOOL2', -0.5, -0.5],
        ['BOOL2', 5, 5],
        ['BOOL2', -3, -3],
    ]


def info_add_info():
    return [
        ['FLOAT1', 'FLOAT2', -1],
        ['FLOAT1', 'INT2', -1.5],
        ['FLOAT1', 'BOOL1', 2.5],
        ['FLOAT1', 'BOOL2', 1.5],

        ['INT1', 'FLOAT2', -0.5],
        ['INT1', 'INT2', -1],
        ['INT1', 'BOOL1', 3],
        ['INT1', 'BOOL2', 2],

        ['BOOL1', 'FLOAT2', -1.5],
        ['BOOL1', 'INT2', -2],

        ['BOOL2', 'FLOAT2', -2.5],
        ['BOOL2', 'INT2', -3],

        ['BOOL1', 'BOOL1', 2],
        ['BOOL2', 'BOOL2', 0],
        ['BOOL1', 'BOOL2', 1],
        ['BOOL2', 'BOOL1', 1],

    ]


def info_iadd_built_in_type():
    return [
        ['FLOAT1', 1.5, 3],
        ['FLOAT1', -0.5, 1],
        ['FLOAT1', 5, 6.5],
        ['FLOAT1', -3, -1.5],

        ['INT1', 5, 7],
        ['INT1', -3, -1],
    ]


def info_iadd_info():
    return [
        ['FLOAT1', 'FLOAT2', -1],
        ['FLOAT1', 'INT2', -1.5],
        ['FLOAT1', 'BOOL1', 2.5],
        ['FLOAT1', 'BOOL2', 1.5],

        ['INT1', 'INT2', -1],
        ['INT1', 'BOOL1', 3],
        ['INT1', 'BOOL2', 2],
    ]
