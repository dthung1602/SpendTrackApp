from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Union, TypeVar

from django.conf import settings
from django.db import models
from django.db.models import QuerySet
from django.db.models import Sum
from django.db.models.functions import Extract

NullableDate = TypeVar('NullableDate', Union[str, None], datetime)


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
        if len(self.parent.ancestors) + 2 > settings.MODEL_CATEGORY_HIERARCHY_MAX_DEPTH:
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
                           category_name: Optional[str] = None,
                           limit: int = settings.VIEW_SUMMARIZE_DATE_RANGE_DEFAULT_PAGE_SIZE,
                           prefetch: bool = True) -> QuerySet:
        """
        Find entries between start_date and end_date (inclusive) which belong to the given category name

        :param start_date:
        :param end_date:
            - can be None, datetime objects or a string 'YYYY-mm-dd'
            - time info will be discarded and replaced with 23:59:59 for end_date and 00:00:00 for start_date
            - if start_date (or end_date) is None, it will show_drop_down from the beginning (or till the ending)
        :param category_name: name of the category. If not given, all categories are selected
        :param limit: maximum number of entries to return. No limit is set if -1 is given
        :param prefetch: whether to prefetch associated categories
        """
        start_date = cls.__modify_start_date(start_date)
        end_date = cls.__modify_end_date(end_date)
        result = cls.objects.filter(date__range=(start_date, end_date)).order_by('date')
        if category_name is not None:
            result = result.filter(categories__name=category_name)
        if prefetch:
            result = result.prefetch_related("categories", "leaf_category")
        return result[:limit] if limit >= 0 else result

    @classmethod
    def find_by_year(cls,
                     year: int,
                     category_name: Optional[str] = None,
                     limit: int = settings.VIEW_SUMMARIZE_YEAR_DEFAULT_PAGE_SIZE,
                     prefetch: bool = True) -> QuerySet:
        """
        Find entries in the given year

        :param year: four-digits year
        :param category_name: name of the category. If not given, all categories are selected
        :param limit: maximum number of entries to return. No limit is set if -1 is given
        :param prefetch: whether to prefetch associated categories
        """
        result = cls.objects.filter(date__year=year).order_by('date')
        if category_name is not None:
            result = result.filter(categories__name=category_name)
        if prefetch:
            result = result.prefetch_related("categories", "leaf_category")
        return result[:limit] if limit >= 0 else result

    @classmethod
    def find_by_month(cls,
                      year: int,
                      month: int,
                      category_name: Optional[str] = None,
                      limit: int = settings.VIEW_SUMMARIZE_MONTH_DEFAULT_PAGE_SIZE,
                      prefetch: bool = True) -> QuerySet:
        """
        Find entries in the given month in year
        
        :param year: four-digits year
        :param month: 1, 2, ... 12
        :param category_name: name of the category. If not given, all categories are selected
        :param limit: maximum number of entries to return. No limit is set if -1 is given
        :param prefetch: whether to prefetch associated categories
        """
        result = cls.objects.filter(date__year=year, date__month=month).order_by('date')
        if category_name is not None:
            result = result.filter(categories__name=category_name)
        if prefetch:
            result = result.prefetch_related("categories", "leaf_category")
        return result[:limit] if limit >= 0 else result

    @classmethod
    def find_by_week(cls,
                     isoyear: int,
                     week: int,
                     category_name: Optional[str] = None,
                     limit: int = settings.VIEW_SUMMARIZE_WEEK_DEFAULT_PAGE_SIZE,
                     prefetch: bool = True) -> QuerySet:
        """
        Find entries in the given week in year

        :param isoyear: four-digits ISO8601 year of the actual datetime object
        :param week: ISO8601 week in year
        :param category_name: name of the category. If not given, all categories are selected
        :param limit: maximum number of entries to return. No limit is set if -1 is given
        :param prefetch: whether to prefetch associated categories
        """
        result = cls.objects.filter(date__isoyear=isoyear, date__week=week).order_by('date')
        if category_name is not None:
            result = result.filter(categories__name=category_name)
        if prefetch:
            result = result.prefetch_related("categories", "leaf_category")
        return result[:limit] if limit >= 0 else result

    ##############################################################
    #                 CALCULATE TOTAL METHODS                    #
    ##############################################################

    @classmethod
    def total_by_date_range(cls,
                            start_date: NullableDate = None,
                            end_date: NullableDate = None,
                            category_name: Optional[str] = None) -> float:
        """
        Find total value of entries between start_date and end_date (inclusive) which belong to the given category name

        :param start_date:
        :param end_date:
            - can be None, datetime objects or a string 'YYYY-mm-dd'
            - time info will be discarded and replaced with 23:59:59 for end_date and 00:00:00 for start_date
            - if start_date (or end_date) is None, it will show_drop_down from the beginning (or till the ending)
        :param category_name: name of the category. If not given, all categories are selected
         """
        result = cls.find_by_date_range(start_date, end_date, category_name, -1, False).order_by()
        result = result.aggregate(total=Sum('value'))['total']
        return result if result is not None else 0

    @classmethod
    def total_by_year(cls,
                      year: int,
                      category_name: Optional[str] = None) -> float:
        """
        Find total value of entries in the given year

        :param year: four-digits year
        :param category_name:
                - name of the category
                - if it is not given, all categories are selected
        """
        result = cls.find_by_year(year, category_name, -1, False).order_by()
        result = result.aggregate(total=Sum('value'))['total']
        return result if result is not None else 0

    @classmethod
    def total_by_month(cls,
                       year: int,
                       month: int,
                       category_name: Optional[str] = None) -> float:
        """
        Find total value of entries in the given month in year

        :param year: four-digits year
        :param month: 1, 2, ... 12
        :param category_name:
                - name of the category
                - if it is not given, all categories are selected
        """
        result = cls.find_by_month(year, month, category_name, -1, False).order_by()
        result = result.aggregate(total=Sum('value'))['total']
        return result if result is not None else 0

    @classmethod
    def total_by_week(cls,
                      isoyear: int,
                      week: int,
                      category_name: Optional[str] = None) -> float:
        """
        Find total value of entries in the given week in year

        :param isoyear: four-digits ISO8601 year of the actual datetime object
        :param week: ISO8601 week in year
        :param category_name:
                - name of the category
                - if it is not given, all categories are selected
        """
        result = cls.find_by_week(isoyear, week, category_name, -1, False).order_by()
        result = result.aggregate(total=Sum('value'))['total']
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
        if isinstance(start_date, datetime):
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
        if isinstance(end_date, datetime):
            return end_date.strftime("%Y-%m-%d 23:59:59")
        if isinstance(end_date, str):
            datetime.strptime(end_date, "%Y-%m-%d")
            return end_date + " 23:59:59"
        raise TypeError('Invalid datetime')


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
