from datetime import datetime

from django.db import models
from django.db.models import Sum
from django.db.models.functions import Extract


@models.DateTimeField.register_lookup
class ExtractISOYear(Extract):
    """Enable isoyear filter"""
    lookup_name = 'isoyear'


class Category(models.Model):
    """
    A class represents spending category
    Categories are organized to a forest:
        - Each Entry belongs only to one leaf category and its ancestors
        - Each Entry belongs only to one tree
    """

    name = models.CharField(
        max_length=25,
        unique=True
    )

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    __children = None

    __ancestors = None

    __ancestors_ids = None

    @property
    def children(self):
        if self.__children is None:
            self.__children = Category.objects.filter(parent=self).order_by("name")
        return self.__children

    @property
    def ancestors(self):
        if self.__ancestors is None:
            self.__ancestors = []
            category = self
            while category.parent is not None:
                self.__ancestors.append(category.parent)
                category = category.parent
        return self.__ancestors

    @property
    def ancestors_ids(self):
        if self.__ancestors_ids is None:
            self.__ancestors_ids = [cat.id for cat in self.ancestors]
        return self.__ancestors_ids

    @property
    def is_leaf(self):
        """Whether a category has no children"""
        return len(self.children) == 0

    def __str__(self):
        return self.name

    @classmethod
    def get_leaf_category(cls, category_id):
        try:
            category = Category.objects.get(pk=category_id)
            if not category.is_leaf:
                raise ValueError
            return category
        except (ValueError, Category.DoesNotExist):
            return None

    @classmethod
    def get_root_categories(cls):
        return cls.objects.filter(parent__isnull=True).order_by("name")


class Entry(models.Model):
    """A class represents all changes in the balance"""

    date = models.DateTimeField()

    content = models.CharField(
        max_length=250
    )

    value = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.date.strftime("[%Y-%m-%d] ") + self.content[:20].ljust(20) + " " + str(self.value)

    def change_category(self, category):
        """
        Clear all old categories and add category_id + its ancestors' ids
        :raise ValueError when category is not leaf
        """
        if not category.is_leaf:
            raise ValueError('Category is not leaf')
        to_add_category_ids = [category.id] + category.ancestors_ids
        self.categories.clear()
        self.categories.add(*to_add_category_ids)

    ##############################################################
    #                       FIND METHODS                         #
    ##############################################################

    @classmethod
    def find_by_date_range(cls, start_date=None, end_date=None, category_name=None):
        """
        Find entries between start_date and end_date (inclusive) which belong to the given category name
        :param start_date:
        :param end_date:
            - can be None, datetime objects or a string 'YYYY-mm-dd'
            - time info will be discarded and replaced with 23:59:59 for end_date and 00:00:00 for start_date
            - if start_date (or end_date) is None, it will select from the beginning (or till the ending)
        :param category_name:
            - name of the category
            - if it is not given, all categories are selected
        :return QuerySet
        """
        start_date = cls.__modify_start_date(start_date)
        end_date = cls.__modify_end_date(end_date)
        result = cls.objects.filter(date__range=(start_date, end_date)).order_by('date')
        if category_name is not None:
            result = result.filter(categories__name=category_name)
        return result

    @classmethod
    def find_by_year(cls, year, category_name=None):
        """
        Find entries in the given year
        :param year: four-digits year
        :param category_name:
                - name of the category
                - if it is not given, all categories are selected
        :return: QuerySet
        """
        result = cls.objects.filter(date__year=year).order_by('date')
        if category_name is not None:
            result = result.filter(categories__name=category_name)
        return result

    @classmethod
    def find_by_month(cls, year, month, category_name=None):
        """
        Find entries in the given month in year
        :param year: four-digits year
        :param month: jan=1, feb=2, ...
        :param category_name:
                - name of the category
                - if it is not given, all categories are selected
        :return: QuerySet
        """
        result = cls.objects.filter(date__year=year, date__month=month).order_by('date')
        if category_name is not None:
            result = result.filter(categories__name=category_name)
        return result

    @classmethod
    def find_by_week(cls, isoyear, week, category_name=None):
        """
        Find entries in the given week in year
        :param isoyear: four-digits ISO8601 year of the actual datetime object
        :param week: ISO8601 week in year
        :param category_name:
                - name of the category
                - if it is not given, all categories are selected
        :return: QuerySet
        """
        result = cls.objects.filter(date__isoyear=isoyear, date__week=week).order_by('date')
        if category_name is not None:
            result = result.filter(categories__name=category_name)
        return result

    ##############################################################
    #                 CALCULATE TOTAL METHODS                    #
    ##############################################################

    @classmethod
    def total_by_date_range(cls, start_date=None, end_date=None, category_name=None):
        """
        Find total value of entries between start_date and end_date (inclusive) which belong to the given category name
        :param start_date:
        :param end_date:
            - can be None, datetime objects or a string 'YYYY-mm-dd'
            - time info will be discarded and replaced with 23:59:59 for end_date and 00:00:00 for start_date
            - if start_date (or end_date) is None, it will select from the beginning (or till the ending)
        :param category_name:
            - name of the category
            - if it is not given, all categories are selected
        :return float
         """
        result = cls.find_by_date_range(start_date, end_date, category_name).order_by()
        result = result.aggregate(total=Sum('value'))['total']
        return result if result is not None else 0

    @classmethod
    def total_by_year(cls, year, category_name=None):
        """
        Find total value of entries in the given year
        :param year: four-digits year
        :param category_name:
                - name of the category
                - if it is not given, all categories are selected
        :return: float
        """
        result = cls.find_by_year(year, category_name).order_by()
        result = result.aggregate(total=Sum('value'))['total']
        return result if result is not None else 0

    @classmethod
    def total_by_month(cls, year, month, category_name=None):
        """
        Find total value of entries in the given month in year
        :param year: four-digits year
        :param month: jan=1, feb=2, ...
        :param category_name:
                - name of the category
                - if it is not given, all categories are selected
        :return: float
        """
        result = cls.find_by_month(year, month, category_name).order_by()
        result = result.aggregate(total=Sum('value'))['total']
        return result if result is not None else 0

    @classmethod
    def total_by_week(cls, isoyear, week, category_name=None):
        """
        Find total value of entries in the given week in year
        :param isoyear: four-digits ISO8601 year of the actual datetime object
        :param week: ISO8601 week in year
        :param category_name:
                - name of the category
                - if it is not given, all categories are selected
        :return: float
        """
        result = cls.find_by_week(isoyear, week, category_name).order_by()
        result = result.aggregate(total=Sum('value'))['total']
        return result if result is not None else 0

    ##############################################################
    #                      HELPER METHODS                        #
    ##############################################################

    @staticmethod
    def __modify_start_date(start_date):
        """
        Helper method to modify start date
        :raise TypeError when start_date is not string or datetime object
        :raise ValueError when start_date is a string but does not match "%Y-%m-%d"
        """
        if start_date is None:
            return '1000-1-1'
        if isinstance(start_date, datetime):
            return start_date.replace(hour=0, minute=0, second=0)
        if isinstance(start_date, str):
            return start_date + ' 0:0:0'
        raise TypeError('Invalid datetime')

    @staticmethod
    def __modify_end_date(end_date):
        """
        Helper method to modify end_date
        :raise TypeError when start_date is not string or datetime object
        :raise ValueError when start_date is a string but does not match "%Y-%m-%d"
        """
        if end_date is None:
            return '9999-12-31'
        if isinstance(end_date, datetime):
            return end_date.replace(hour=23, minute=59, second=59)
        if isinstance(end_date, str):
            return end_date + ' 23:59:59'
        raise TypeError('Invalid datetime')


class Info(models.Model):
    """
    A class used to stores information
        - name: name of the info
        - value: string represent the info
        - value_type: type of the info (integer, float, string or boolean)
    """

    name = models.CharField(
        max_length=100,
        unique=True
    )

    value = models.CharField(
        max_length=500
    )

    value_type = models.CharField(
        max_length=1,
        choices=(('i', 'integer'), ('f', 'float'), ('s', 'string'), ('b', 'boolean'))
    )

    __converter = {
        'i': int,
        'f': float,
        's': str,
        'b': lambda value: value[0] in ['t', 'T', '1'] if isinstance(value, str) else value
    }

    def get_actual_value(self):
        """Get the actual info in the correct type, NOT as a string as in database"""
        return self.__converter[self.value_type](self.value)

    @classmethod
    def get(cls, name):
        """Get the actual info with the given name in the correct type"""
        return cls.objects.get(name=name).get_actual_value()

    @classmethod
    def set(cls, name, value):
        """
        Set value of the info with given name and save to database
        :raise ValueError iF value is invalid
        """
        info = cls.objects.get(name=name)
        str_value = str(value)
        if value != cls.__converter[info.value_type](str_value):
            raise ValueError()
        info.value = str_value
        info.save()
