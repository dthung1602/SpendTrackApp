from datetime import datetime

from django.db import models
from django.db.models.functions import Extract


@models.DateTimeField.register_lookup
class ExtractISOYear(Extract):
    lookup_name = 'isoyear'


class Category(models.Model):
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

    def __str__(self):
        return "id = " + str(self.id) + " " + self.name

    def get_ancestor_ids(self):
        ancestor_ids = []
        category = self
        while category.parent is not None:
            ancestor_ids.append(category.parent.id)
            category = category.parent
        return ancestor_ids

    def is_leaf(self):
        return Category.objects.filter(parent=self).count() == 0


class Entry(models.Model):
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

    def change_category(self, id):
        category = Category.objects.get(pk=id)
        to_add_category_ids = [id] + category.get_ancestor_ids()
        self.categories.clear()
        self.categories.add(*to_add_category_ids)

    @staticmethod
    def find_by_date_range(start_date=None, end_date=None):
        start_date = Entry.mod_start_date(start_date)
        end_date = Entry.mod_end_date(end_date)
        return Entry.objects.filter(date__range=(start_date, end_date)).order_by('date')

    @staticmethod
    def find_by_year(year):
        return Entry.objects.filter(date__year=year).order_by('date')

    @staticmethod
    def find_by_month(year, month):
        return Entry.objects.filter(date__year=year, date__month=month).order_by('date')

    @staticmethod
    def find_by_week(isoyear, week):
        return Entry.objects.filter(date__isoyear=isoyear, date__week=week).order_by('date')

    @staticmethod
    def mod_start_date(start_date):
        if start_date is None:
            return '1000-1-1'
        if isinstance(start_date, datetime):
            return start_date.replace(hour=0, minute=0, second=0)
        if isinstance(start_date, str):
            return start_date + ' 0:0:0'
        raise ValueError('Invalid datetime')

    @staticmethod
    def mod_end_date(end_date):
        if end_date is None:
            return '9999-12-31'
        if isinstance(end_date, datetime):
            return end_date.replace(hour=23, minute=59, second=59)
        if isinstance(end_date, str):
            return end_date + ' 23:59:59'
        raise ValueError('Invalid datetime')
