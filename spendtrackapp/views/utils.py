import datetime as dt
import re
from datetime import datetime
from math import ceil

from dateutil.parser import isoparse
from django.conf import settings
from django.shortcuts import render as rd

##############################################################
#                        DATE TIME                           #
##############################################################

month_full_names = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

month_abr_names = [
    'jan', 'feb', 'mar', 'apr', 'may', 'jun',
    'jul', 'aug', 'sep', 'oct', 'nov', 'dec'
]


def same_date(date1: datetime, date2: datetime) -> bool:
    """Check whether two given datetime object are in the same date"""

    return date1.day == date2.day and date1.month == date2.month and date1.year == date2.year


def daterange(date, to=None, step=dt.timedelta(days=1)):
    """
    Ref: https://github.com/zacharyvoase/daterange/
    Similar to the built-in ``xrange()``, only for datetime objects.

    If called with just a ``datetime`` object, it will keep yielding values
    forever, starting with that date/time and counting in steps of 1 day.

    If the ``to`` keyword is provided, it will count up to and INCLUDING
    that date/time (again, in steps of 1 day by default).

    If the ``step`` keyword is provided, this will be used as the step size
    instead of the default of 1 day. It should be either an instance of
    ``datetime.timedelta``, an integer, a string representing an integer, or
    a string representing a ``delta()`` value (consult the documentation for
    ``delta()`` for more information). If it is an integer (or string thereof)
    then it will be interpreted as a number of days. If it is not a simple
    integer string, then it will be passed to ``delta()`` to get an instance
    of ``datetime.timedelta()``.

    Note that, due to the similar interfaces of both objects, this function
    will accept both ``datetime.datetime`` and ``datetime.date`` objects. If
    a date is given, then the values yielded will be dates themselves. A
    caveat is in order here: if you provide a date, the step should have at
    least a ‘days’ component; otherwise the same date will be yielded forever.
    """

    if isinstance(date, str):
        date = isoparse(date)

    if to is None:
        condition = lambda d: True
    else:
        if isinstance(to, str):
            to = isoparse(to)
        condition = lambda d: (d <= to)

    if isinstance(step, int):
        # By default, integers are interpreted in days. For more granular
        # steps, use a `datetime.timedelta()` instance.
        step = dt.timedelta(days=step)
    elif isinstance(step, str):
        # If the string
        if re.match(r'^(\d+)$', str(step)):
            step = dt.timedelta(days=int(step))
        else:
            try:
                step = StrTimeDelta(step)
            except ValueError:
                pass

    if not isinstance(step, dt.timedelta):
        raise TypeError('Invalid step value: %r' % (step,))

    # The main generation loop.
    while condition(date):
        yield date
        date += step


class StrTimeDelta(object):
    """
    Ref: https://github.com/zacharyvoase/daterange/
    Build instances of ``datetime.timedelta`` using short, friendly strings.

    ``delta()`` allows you to build instances of ``datetime.timedelta`` in
    fewer characters and with more readability by using short strings instead
    of a long sequence of keyword arguments.

    A typical (but very precise) spec string looks like this:

        '1 day, 4 hours, 5 minutes, 3 seconds, 120 microseconds'

    ``datetime.timedelta`` doesn’t allow deltas containing months or years,
    because of the differences between different months, leap years, etc., so
    this function doesn’t support them either.

    The parser is very simple; it takes a series of comma-separated values,
    each of which represents a number of units of time (such as one day,
    four hours, five minutes, et cetera). These ‘specifiers’ consist of a
    number and a unit of time, optionally separated by whitespace. The units
    of time accepted are (case-insensitive):

        * Days ('d', 'day', 'days')
        * Hours ('h', 'hr', 'hrs', 'hour', 'hours')
        * Minutes ('m', 'min', 'mins', 'minute', 'minutes')
        * Seconds ('s', 'sec', 'secs', 'second', 'seconds')
        * Microseconds ('ms', 'microsec', 'microsecs' 'microsecond',
          'microseconds')

    If an illegal specifier is present, the parser will raise a ValueError.

    This utility is provided as a class, but acts as a function (using the
    ``__new__`` method). This is so that the names and aliases for units are
    stored on the class object itself: as ``UNIT_NAMES``, which is a mapping
    of names to aliases, and ``UNIT_ALIASES``, the converse.
    """

    UNIT_NAMES = {
        #  unit_name: unit_aliases
        'days': 'd day'.split(),
        'hours': 'h hr hrs hour'.split(),
        'minutes': 'm min mins minute'.split(),
        'seconds': 's sec secs second'.split(),
        'microseconds': 'ms microsec microsecs microsecond'.split(),
    }

    # Turn `UNIT_NAMES` inside-out, so that unit aliases point to canonical
    # unit names.
    UNIT_ALIASES = {}

    for cname, aliases in UNIT_NAMES.items():
        for alias in aliases:
            UNIT_ALIASES[alias] = cname
        # Make the canonical unit name point to itself.
        UNIT_ALIASES[cname] = cname

    def __new__(cls, string):
        specifiers = (specifier.strip() for specifier in string.split(','))
        kwargs = {}

        for specifier in specifiers:
            match = re.match(r'^(\d+)\s*(\w+)$', specifier)
            if not match:
                raise ValueError('Invalid delta specifier: %r' % (specifier,))

            number, unit_alias = match.groups()
            number, unit_alias = int(number), unit_alias.lower()

            unit_cname = cls.UNIT_ALIASES.get(unit_alias)
            if not unit_cname:
                raise ValueError('Invalid unit: %r' % (unit_alias,))
            kwargs[unit_cname] = kwargs.get(unit_cname, 0) + number

        return dt.timedelta(**kwargs)


def is_valid_iso_week(year: str, week: str) -> bool:
    """Check whether the given ISO week & ISO year is valid"""

    try:
        isoparse("%iW%02i" % (int(year), int(week)))
        return True
    except ValueError:
        return False


##############################################################
#                          ARRAY                             #
##############################################################

def group_array(arr, group_size):
    """Divide arr into groups with size at least group_size"""

    arr = list(arr)
    if group_size > 0:
        return [arr[i * group_size:i * group_size + group_size] for i in range(ceil(len(arr) / group_size))]
    return [arr]


def arr_to_js_str(arr, converter):
    """Convert a python array to a string represent Javascript array"""

    result = str([converter(i) for i in arr])
    if converter is bool:
        return result.replace('T', 't').replace('F', 'f')
    return result


##############################################################
#                         OTHERS                             #
##############################################################

def render(request, template_name, context=None, content_type=None, status=None, using=None):
    """Override render function to add information to context for base.html"""

    if context is None:
        context = {}
    context['now'] = datetime.now()
    context['app_version'] = settings.APP_VERSION
    context['contact_email'] = settings.CONTACT_EMAIL
    context['contact_github'] = settings.CONTACT_GITHUB
    context['contact_facebook'] = settings.CONTACT_FACEBOOK

    return rd(request, template_name, context, content_type, status, using)


def get_post(request):
    post = request.POST.copy()
    post['user'] = request.user.id
    return post
