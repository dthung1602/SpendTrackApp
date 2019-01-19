from __future__ import annotations

import calendar
from datetime import date, timedelta
from math import fabs

from dateutil.parser import isoparse
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models import QuerySet

from .category import Category
from .entry import Entry


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
        null=True,
        blank=True
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

    def __str__(self):
        return self.name

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

    @property
    # TODO add test
    def target(self) -> str:
        """A string describes the plan"""

        category_name = f'"{self.category.name}"' if self.category is not None else "all categories"
        compare = {"<": "less than", ">": "greater than", "=": "equal to"}[self.compare]
        return "Total in " + category_name + " is " + compare + " " + str(self.planned_total)

    @property
    def start_date_iso(self):
        return self.start_date.isoformat()

    @property
    def end_date_iso(self):
        return self.end_date.isoformat()

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

        year = int(year)
        if isinstance(month, str):
            month = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                     'jul', 'aug', 'sep', 'oct', 'nov', 'dec'].index(month.lower()) + 1

        last_day = calendar.monthrange(year, month)[1]
        return cls.get_plans_in_date_range(
            "{}-{}-01".format(year, month),
            "{}-{}-{}".format(year, month, last_day)
        )

    @classmethod
    def get_plans_in_week(cls, year, week) -> QuerySet:
        """Get all plans that overlaps the given week"""

        monday = isoparse("%iW%02i" % (int(year), int(week)))
        sunday = monday + timedelta(days=6)
        return cls.get_plans_in_date_range(
            monday.strftime("%Y-%m-%d"),
            sunday.strftime("%Y-%m-%d")
        )
