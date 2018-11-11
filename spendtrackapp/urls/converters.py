from datetime import datetime

from django.urls import register_converter


class TwoDigitWeekConverter:
    regex = '[0-9]{2}'

    def to_python(self, value):
        value = int(value)
        if not (0 < value < 54):
            raise ValueError
        return value

    def to_url(self, value):
        value = int(value)
        if not 1 <= value <= 53:
            raise ValueError("Week number must be between 1 and 53")
        return '%02d' % value


class ThreeCharMonthConverter:
    regex = '[a-z]{3}'
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    def to_python(self, value):
        pos = self.months.index(value.lower())
        if pos == -1:
            raise ValueError
        return pos + 1

    def to_url(self, value):
        if isinstance(value, str) and value.lower() in self.months:
            return value.lower()
        value = int(value)
        if not 1 <= value <= 12:
            raise ValueError("Month must be between 1 and 12")
        return self.months[int(value) - 1]


class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        if not 1000 <= int(value) <= 9999:
            raise ValueError("Year must be between 1000 and 9999")
        return str(value)


class DateConverter:
    regex = '[0-9-]{10}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d')
        elif isinstance(value, str):
            return value
        else:
            raise TypeError


register_converter(TwoDigitWeekConverter, 'ww')
register_converter(ThreeCharMonthConverter, 'mmm')
register_converter(FourDigitYearConverter, 'yyyy')
register_converter(DateConverter, 'date')
