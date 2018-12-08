from __future__ import annotations

import calendar
from datetime import datetime, date, timedelta
from math import fabs
from typing import List, Optional, Union, TypeVar

from dateutil.parser import isoparse
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models import QuerySet
from django.db.models import Sum
from django.db.models.functions import Extract

NullableDate = TypeVar('NullableDate', Union[str, None], datetime, date)


# noinspection PyAbstractClass
@models.DateTimeField.register_lookup
class ExtractISOYear(Extract):
    """Enable isoyear filter"""

    lookup_name = 'isoyear'


class Category(models.Model):
    """
    A class represents spending category
    Categories are organized to a forest:
        - Each Entry belongs only to one leaf category and all of its ancestors
        - Each Entry belongs only to one tree
    """

    name = models.CharField(
        max_length=25,
        unique=True
    )
    """Name of the category. Must be unique."""

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    """Parent of this category. Root categories has no parent."""

    _children = None

    _ancestors = None

    _ancestors_ids = None

    @property
    def children(self) -> QuerySet:
        """List of children of the category, order by name"""

        if self._children is None:
            self._children = Category.objects.filter(parent=self).order_by("name")
        return self._children

    @property
    def ancestors(self) -> List[Category]:
        """List of all ancestors of the category, order by increasing distance to this category"""

        if self._ancestors is None:
            self._ancestors = []
            category = self
            while category.parent is not None:
                self._ancestors.append(category.parent)
                category = category.parent
        return self._ancestors

    @property
    def ancestors_ids(self) -> List[int]:
        """List of all ancestors' ids"""

        if self._ancestors_ids is None:
            self._ancestors_ids = [cat.id for cat in self.ancestors]
        return self._ancestors_ids

    @property
    def is_leaf(self) -> bool:
        """Whether a category has no children"""

        return len(self.children) == 0

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """Override save method to validate category before changes are made in DB"""

        if self.parent is not None and len(self.parent.ancestors) + 2 > settings.MODEL_CATEGORY_HIERARCHY_MAX_DEPTH:
            raise ValueError("MODEL_CATEGORY_HIERARCHY_MAX_DEPTH exceeded")
        super().save(force_insert, force_update, using, update_fields)

    @classmethod
    def get_leaf_category(cls, category_id: int) -> Optional[Category]:
        """
        Return None if category_id is invalid or the category is not leaf
        Otherwise return the category with matching id
        """

        try:
            category = Category.objects.get(pk=category_id)
            if not category.is_leaf:
                raise ValueError
            return category
        except (ValueError, Category.DoesNotExist):
            return None

    @classmethod
    def get_root_categories(cls) -> QuerySet:
        """Return a list of all root categories in database, order by name"""

        return cls.objects.filter(parent__isnull=True).order_by("name")


CategoryIdentifier = TypeVar('CategoryIdentifier', Optional[str], Category, int)


class Entry(models.Model):
    """A class represents all changes in the balance"""

    date = models.DateTimeField()
    """When the item is bought"""

    content = models.CharField(
        max_length=250
    )
    """Name of the item"""

    value = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    """Price of the item"""

    categories = models.ManyToManyField(Category)
    """
    Category of the item (e.g food, travel)
    Any item must belong to EXACTLY ONE leaf category
    """

    leaf_category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="leaf_category",
        null=True
    )
    """The category stands lowest in the hierarchy (has no children) that the entry belongs to"""

    @property
    def formatted_date(self):
        return self.date.strftime("%a %b %d, %I %p")

    def __str__(self):
        return self.date.strftime("[%Y-%m-%d] ") + self.content[:20].ljust(20) + " " + str(self.value)

    def change_category(self, category: Category) -> None:
        """
        Clear all old categories and add category_id + its ancestors' ids
        
        :raise ValueError when category is not leaf
        """

        if not category.is_leaf:
            raise ValueError('Category is not leaf')
        to_add_category_ids = [category.id] + category.ancestors_ids
        self.categories.clear()
        self.categories.add(*to_add_category_ids)
        self.leaf_category = category

    ##############################################################
    #                       FIND METHODS                         #
    ##############################################################

    @classmethod
    def find_by_date_range(cls,
                           start_date: NullableDate = None,
                           end_date: NullableDate = None,
                           category: CategoryIdentifier = None,
                           limit: int = -1,
                           prefetch: bool = True) -> QuerySet:
        """
        Find entries between start_date and end_date (inclusive) which belong to the given category name

        :param start_date:
        :param end_date:
            - can be None, datetime objects or a string 'YYYY-mm-dd'
            - time info will be discarded and replaced with 23:59:59 for end_date and 00:00:00 for start_date
            - if start_date (or end_date) is None, it will show_drop_down from the beginning (or till the ending)
        :param category: category object or its name or id. If not given, all categories are selected
        :param limit: maximum number of entries to return. No limit is set if -1 is given
        :param prefetch: whether to prefetch associated categories
        """

        start_date = cls.__modify_start_date(start_date)
        end_date = cls.__modify_end_date(end_date)

        result = cls.objects.filter(date__range=(start_date, end_date)).order_by('date')
        result = cls.__filter_category(result, category)
        result = cls.__prefetch(result, prefetch)

        return result[:limit] if limit >= 0 else result

    @classmethod
    def find_by_year(cls,
                     year: int,
                     category: CategoryIdentifier = None,
                     limit: int = -1,
                     prefetch: bool = True) -> QuerySet:
        """
        Find entries in the given year

        :param year: four-digits year
        :param category: category object or its name or id. If not given, all categories are selected
        :param limit: maximum number of entries to return. No limit is set if -1 is given
        :param prefetch: whether to prefetch associated categories
        """

        result = cls.objects.filter(date__year=year).order_by('date')
        result = cls.__filter_category(result, category)
        result = cls.__prefetch(result, prefetch)

        return result[:limit] if limit >= 0 else result

    @classmethod
    def find_by_month(cls,
                      year: int,
                      month: int,
                      category: CategoryIdentifier = None,
                      limit: int = -1,
                      prefetch: bool = True) -> QuerySet:
        """
        Find entries in the given month in year
        
        :param year: four-digits year
        :param month: 1, 2, ... 12
        :param category: category object or its name or id. If not given, all categories are selected
        :param limit: maximum number of entries to return. No limit is set if -1 is given
        :param prefetch: whether to prefetch associated categories
        """

        result = cls.objects.filter(date__year=year, date__month=month).order_by('date')
        result = cls.__filter_category(result, category)
        result = cls.__prefetch(result, prefetch)

        return result[:limit] if limit >= 0 else result

    @classmethod
    def find_by_week(cls,
                     isoyear: int,
                     week: int,
                     category: CategoryIdentifier = None,
                     limit: int = - 1,
                     prefetch: bool = True) -> QuerySet:
        """
        Find entries in the given week in year

        :param isoyear: four-digits ISO8601 year of the actual datetime object
        :param week: ISO8601 week in year
        :param category: category object or its name or id. If not given, all categories are selected
        :param limit: maximum number of entries to return. No limit is set if -1 is given
        :param prefetch: whether to prefetch associated categories
        """

        result = cls.objects.filter(date__isoyear=isoyear, date__week=week).order_by('date')
        result = cls.__filter_category(result, category)
        result = cls.__prefetch(result, prefetch)

        return result[:limit] if limit >= 0 else result

    ##############################################################
    #                 CALCULATE TOTAL METHODS                    #
    ##############################################################

    @classmethod
    def total_by_date_range(cls,
                            start_date: NullableDate = None,
                            end_date: NullableDate = None,
                            category: CategoryIdentifier = None) -> float:
        """
        Find total value of entries between start_date and end_date (inclusive) which belong to the given category name

        :param start_date:
        :param end_date:
            - can be None, datetime objects or a string 'YYYY-mm-dd'
            - time info will be discarded and replaced with 23:59:59 for end_date and 00:00:00 for start_date
            - if start_date (or end_date) is None, it will show_drop_down from the beginning (or till the ending)
        :param category: category object or its name or id. If not given, all categories are selected
         """

        result = cls.find_by_date_range(start_date, end_date, category, -1, False).order_by()
        result = cls.__sum(result)
        return result if result is not None else 0

    @classmethod
    def total_by_year(cls,
                      year: int,
                      category: CategoryIdentifier = None) -> float:
        """
        Find total value of entries in the given year

        :param year: four-digits year
        :param category: category object or its name or id. If not given, all categories are selected
        """

        result = cls.find_by_year(year, category, -1, False).order_by()
        result = cls.__sum(result)
        return result if result is not None else 0

    @classmethod
    def total_by_month(cls,
                       year: int,
                       month: int,
                       category: CategoryIdentifier = None) -> float:
        """
        Find total value of entries in the given month in year

        :param year: four-digits year
        :param month: 1, 2, ... 12
        :param category: category object or its name or id. If not given, all categories are selected
        """

        result = cls.find_by_month(year, month, category, -1, False).order_by()
        result = cls.__sum(result)
        return result if result is not None else 0

    @classmethod
    def total_by_week(cls,
                      isoyear: int,
                      week: int,
                      category: CategoryIdentifier = None) -> float:
        """
        Find total value of entries in the given week in year

        :param isoyear: four-digits ISO8601 year of the actual datetime object
        :param week: ISO8601 week in year
        :param category: category object or its name or id. If not given, all categories are selected
        """

        result = cls.find_by_week(isoyear, week, category, -1, False).order_by()
        result = cls.__sum(result)
        return result if result is not None else 0

    ##############################################################
    #                      HELPER METHODS                        #
    ##############################################################

    @staticmethod
    def __modify_start_date(start_date: NullableDate) -> str:
        """
        Helper method to modify start date

        :raise TypeError when start_date is not string or datetime object
        :raise ValueError when start_date is a string but does not match "%Y-%m-%d"
        """

        if start_date is None:
            return '1000-1-1'
        if isinstance(start_date, datetime) or isinstance(start_date, date):
            return start_date.strftime("%Y-%m-%d 0:0:0")
        if isinstance(start_date, str):
            datetime.strptime(start_date, "%Y-%m-%d")
            return start_date + " 0:0:0"
        raise TypeError('Invalid datetime')

    @staticmethod
    def __modify_end_date(end_date: NullableDate) -> str:
        """
        Helper method to modify end_date

        :raise TypeError when start_date is not string or datetime object
        :raise ValueError when start_date is a string but does not match "%Y-%m-%d"
        """

        if end_date is None:
            return '9999-12-31'
        if isinstance(end_date, datetime) or isinstance(end_date, date):
            return end_date.strftime("%Y-%m-%d 23:59:59")
        if isinstance(end_date, str):
            datetime.strptime(end_date, "%Y-%m-%d")
            return end_date + " 23:59:59"
        raise TypeError('Invalid datetime')

    @staticmethod
    def __filter_category(query: QuerySet, category: CategoryIdentifier) -> QuerySet:
        """Helper method to filter out category"""

        if isinstance(category, str):  # search by name
            query = query.filter(categories__name=category)
        elif isinstance(category, int):  # search by id
            query = query.filter(categories__id=category)
        elif isinstance(category, Category):  # search by object
            query = query.filter(categories=category)
        return query

    @staticmethod
    def __prefetch(query: QuerySet, prefetch: bool) -> QuerySet:
        """Helper method to decide whether to prefetch or not"""

        if prefetch:
            query = query.prefetch_related("categories", "leaf_category")
        return query

    @staticmethod
    def __sum(query: QuerySet) -> Optional[float]:
        """Helper method to calculate sum of value fields"""

        return query.aggregate(total=Sum('value'))['total']


class Info(models.Model):
    """A class used to stores information"""

    name = models.CharField(
        max_length=100,
        unique=True
    )
    """Name of the info"""

    value_type = models.CharField(
        max_length=1,
        choices=(('i', 'integer'), ('f', 'float'), ('s', 'string'), ('b', 'boolean'))
    )
    """Type of the info (integer, float, string or boolean)"""

    _value = models.CharField(
        max_length=500
    )
    """String represent the info"""

    _converter = {
        'i': int,
        'f': float,
        's': str,
        'b': lambda value: value[0] in ['t', 'T', '1'] if isinstance(value, str) else value
    }
    """A dictionary matches value_type to a str-to-value_type converter"""

    @property
    def value(self) -> Union[int, float, str, bool]:
        """
        Getter of _value
        Return the actual info in the correct type, NOT as a string as in database
        """
        return self._converter[self.value_type](self._value)

    @value.setter
    def value(self, v: Union[int, float, str, bool]) -> None:
        """
        Setter of _value
        Set convert v to string and set to self._value

        :raise ValueError if v is invalid
        """
        str_value = str(v)
        self._converter[self.value_type](str_value)
        self._value = str_value

    def __str__(self):
        return self.name + "=" + self._value

    @classmethod
    def get(cls, name) -> Info:
        """Get the actual info with the given name in the correct type"""
        return cls.objects.get(name=name)

    @classmethod
    def set(cls, name, value) -> Info:
        """
        Set value of the info with given name and save to database

        :raise ValueError if value is invalid
        """
        info = cls.get(name)
        info.value = value
        info.save()
        return info

    ##############################################################
    #                   OVERRIDDEN OPERATORS                     #
    ##############################################################

    # --------------------- --------------------------------------

    def __iadd__(self, other: Union[Info, float, int, str]) -> Info:
        add_value = other.value if isinstance(other, Info) else other
        self.value = self.value + add_value
        return self

    def __isub__(self, other: Union[Info, float, int, str]) -> Info:
        sub_value = other.value if isinstance(other, Info) else other
        self.value = self.value - sub_value
        return self

    def __imul__(self, other: Union[Info, float, int, str]) -> Info:
        mul = other.value if isinstance(other, Info) else other
        self.value = self.value * mul
        return self

    def __ifloordiv__(self, other: Union[Info, float, int, str]) -> Info:
        div_value = other.value if isinstance(other, Info) else other
        self.value = self.value / div_value
        return self

    def __itruediv__(self, other: Union[Info, float, int, str]) -> Info:
        div_value = other.value if isinstance(other, Info) else other
        self.value = self.value // div_value
        return self

    def __imod__(self, other: Union[Info, float, int, str]) -> Info:
        mod_value = other.value if isinstance(other, Info) else other
        self.value = self.value % mod_value
        return self

    # --------------------- --------------------------------------

    def __add__(self, other: Union[Info, float, int, str]) -> Union[float, int, str]:
        add_value = other.value if isinstance(other, Info) else other
        return self.value + add_value

    def __sub__(self, other: Union[Info, float, int, str]) -> Union[float, int, str]:
        sub_value = other.value if isinstance(other, Info) else other
        return self.value - sub_value

    def __mul__(self, other: Union[Info, float, int, str]) -> Union[float, int, str]:
        mul_value = other.value if isinstance(other, Info) else other
        return self.value * mul_value

    def __floordiv__(self, other: Union[Info, float, int]) -> Union[float, int]:
        div_value = other.value if isinstance(other, Info) else other
        return self.value / div_value

    def __truediv__(self, other: Union[Info, float, int]) -> Union[float, int]:
        div_value = other.value if isinstance(other, Info) else other
        return self.value // div_value

    def __mod__(self, other: Union[Info, float, int]) -> Union[float, int]:
        mod_value = other.value if isinstance(other, Info) else other
        return self.value % mod_value

    # --------------------- --------------------------------------

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        sub_value = other.value if isinstance(other, Info) else other
        return sub_value - self.value

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rfloordiv__(self, other):
        div_value = other.value if isinstance(other, Info) else other
        return div_value / self.value

    def __rtruediv__(self, other):
        div_value = other.value if isinstance(other, Info) else other
        return div_value // self.value

    def __rmod__(self, other):
        div_value = other.value if isinstance(other, Info) else other
        return div_value % self.value


class Plan(models.Model):
    """
    A class to save plans
    """

    name = models.CharField(
        max_length=50,
        null=False
    )
    """Name of the plan"""

    start_date = models.DateField()
    """Plan's start date"""

    end_date = models.DateField()
    """Plan's end date"""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True
    )
    """Category that the plan cares about. 
       This is null if all categories are considered in this plan."""

    planned_total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    """Total amount of money planned to spend in this time period"""

    compare = models.CharField(
        max_length=1,
        choices=(('>', 'gt'), ('=', 'eq'), ('<', 'lt'))
    )
    """Indicates how the actual total should be in comparision with the planned total 
       for the plan to be considered as completed"""

    _entries = None

    _total = None

    @property
    def is_completed(self) -> bool:
        """Whether the plan has been completed successfully"""

        if self.compare == ">":
            return self.total > self.planned_total
        elif self.compare == "<":
            return self.total < self.planned_total
        else:
            if self.planned_total == 0:
                return self.total == 0
            return fabs(self.total / self.planned_total - 1) < settings.MODEL_PLAN_COMPARE_EQUAL_EPSILON

    @property
    def entries(self) -> QuerySet:
        if self._entries is None:
            self._entries = Entry.find_by_date_range(
                self.start_date,
                self.end_date,
                self.category
            )
        return self._entries

    @property
    def total(self) -> float:
        if self._total is None:
            # check if entries cache exists
            if self._entries is not None:
                # yes -> just sum up
                self._total = sum(entry.value for entry in self._entries)
            else:
                # no -> calculate
                self._total = Entry.total_by_date_range(
                    self.start_date,
                    self.end_date,
                    self.category
                )
        return self._total

    @property
    def has_passed(self) -> bool:
        """Whether the plan is in the past, i.e. its end_date has passed"""

        return self.end_date < date.today()

    @classmethod
    def get_current_plans(cls) -> QuerySet:
        """Get all the plans that has not finished"""

        today = date.today()
        return Plan.objects.filter(
            start_date__lte=today,
            end_date__gte=today
        ).order_by("start_date", "end_date", "id")

    @classmethod
    def get_plans_in_date_range(cls, start_date, end_date) -> QuerySet:
        """Get all plans that overlaps the time range"""

        return Plan.objects.filter(
            Q(start_date__lte=end_date) &
            Q(end_date__gte=start_date)
        ).order_by("start_date", "end_date", "id")

    @classmethod
    def get_plans_in_year(cls, year) -> QuerySet:
        """Get all plans that overlaps the given year"""

        year = str(year)
        return cls.get_plans_in_date_range(
            year + "-01-01",
            year + "-12-31"
        )

    @classmethod
    def get_plans_in_month(cls, year, month) -> QuerySet:
        """Get all plans that overlaps the given month"""

        last_day = calendar.monthrange(year, month)[1]
        return cls.get_plans_in_date_range(
            "{}-{}-01".format(year, month),
            "{}-{}-{}".format(year, month, last_day)
        )

    @classmethod
    def get_plans_in_week(cls, year, week) -> QuerySet:
        """Get all plans that overlaps the given week"""

        monday = isoparse("%iW%02i" % (year, week))
        sunday = monday + timedelta(days=6)
        return cls.get_plans_in_date_range(
            monday.strftime("%Y-%m-%d"),
            sunday.strftime("%Y-%m-%d")
        )
