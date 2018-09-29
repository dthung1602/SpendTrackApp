from datetime import datetime

from django.urls import register_converter


class TwoDigitWeekConverter:
    regex = '[0-9]{2}'

    def to_python(self, value):
        value = int(value)
        if not (0 < value < 53):
            raise ValueError
        return value

    def to_url(self, value):
        return '%02d' % value


class ThreeCharMonthConverter:
    regex = '[a-z]{3}'
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    def to_python(self, value):
        pos = self.months.index(value)
        if pos == -1:
            raise ValueError
        return pos + 1

    def to_url(self, value):
        return self.months[value - 1]


class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value


class DateConverter:
    regex = '[0-9-]{10}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')


register_converter(TwoDigitWeekConverter, 'ww')
register_converter(ThreeCharMonthConverter, 'mmm')
register_converter(FourDigitYearConverter, 'yyyy')
register_converter(DateConverter, 'date')
