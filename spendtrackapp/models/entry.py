from __future__ import annotations

from datetime import datetime, date
from typing import Optional
from typing import Union, TypeVar

from django.db import models
from django.db.models import QuerySet
from django.db.models import Sum
from django.db.models.functions import Extract

from .category import Category

NullableDate = TypeVar('NullableDate', Union[str, None], datetime, date)


# noinspection PyAbstractClass
@models.DateTimeField.register_lookup
class ExtractISOYear(Extract):
    """Enable isoyear filter"""

    lookup_name = 'isoyear'


CategoryIdentifier = TypeVar('CategoryIdentifier', Optional[str], Category, int)


class Entry(models.Model):
    """A class represents all changes in the balance"""

    class Meta:
        verbose_name_plural = "Entries"

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
        related_name="leaf_category"
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
