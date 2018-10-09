from django.test import TestCase

from spendtrackapp.models import *
from .provide_data_models import *
from .utils import data_provider


class TestCategory(TestCase):
    fixtures = ['test/category.json']

    @data_provider(category_get_ancestors)
    def test_get_ancestors(self, id, expected_ancestor_ids):
        category = Category.objects.get(pk=id)
        ancestor_ids = category.get_ancestor_ids()
        self.assertCountEqual(expected_ancestor_ids, ancestor_ids)

    @data_provider(category_is_leaf)
    def test_is_leaf(self, id, expected_result):
        category = Category.objects.get(id=id)
        self.assertEqual(expected_result, category.is_leaf())


class TestEntry(TestCase):
    fixtures = ['test/entry_categories.json', 'test/category.json', 'test/entry.json', ]

    @data_provider(entry_change_category)
    def test_change_category(self, entry_id, category_id, expected_ids):
        entry = Entry.objects.get(pk=entry_id)
        entry.change_category(category_id)
        category_ids = [cat.id for cat in entry.categories.all()]
        self.assertCountEqual(expected_ids, category_ids)
        entry.save()
        category_ids = [cat.id for cat in entry.categories.all()]
        self.assertCountEqual(expected_ids, category_ids)

    ##############################################################
    #                       FIND METHODS                         #
    ##############################################################

    @data_provider(entry_find_by_date_range)
    def test_find_by_date_range(self, start_date, end_date, expected_ids):
        entries = Entry.find_by_date_range(start_date, end_date)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_year)
    def test_find_by_year(self, year, expected_ids):
        entries = Entry.find_by_year(year)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_month)
    def test_find_by_month(self, year, month, expected_ids):
        entries = Entry.find_by_month(year, month)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_week)
    def test_find_by_week(self, year, week, expected_ids):
        entries = Entry.find_by_week(year, week)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    ##############################################################
    #                 CALCULATE TOTAL METHODS                    #
    ##############################################################

    @data_provider(entry_total_by_date_range)
    def test_total_by_date_range(self, start_date, end_date, expected_total):
        total = Entry.total_by_date_range(start_date, end_date)
        self.assertAlmostEqual(expected_total, total, 2)

    @data_provider(entry_total_by_year)
    def test_total_by_year(self, year, expected_total):
        total = Entry.total_by_year(year)
        self.assertAlmostEqual(expected_total, total, 2)

    @data_provider(entry_total_by_month)
    def test_total_by_month(self, year, month, expected_total):
        total = Entry.total_by_month(year, month)
        self.assertAlmostEqual(expected_total, total, 2)

    @data_provider(entry_total_by_week)
    def test_total_by_week(self, year, week, expected_total):
        total = Entry.total_by_week(year, week)
        self.assertAlmostEqual(expected_total, total, 2)

    ##############################################################
    #               FIND METHODS WITH CATEGORY                   #
    ##############################################################

    @data_provider(entry_find_by_date_range_with_category)
    def test_find_by_date_range_with_category(self, start_date, end_date, category_name, expected_ids):
        entries = Entry.find_by_date_range(start_date, end_date, category_name)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_year_with_category)
    def test_find_by_year_with_category(self, year, category_name, expected_ids):
        entries = Entry.find_by_year(year, category_name)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_month_with_category)
    def test_find_by_month_with_category(self, year, month, category_name, expected_ids):
        entries = Entry.find_by_month(year, month, category_name)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_week_with_category)
    def test_find_by_week_with_category(self, year, week, category_name, expected_ids):
        entries = Entry.find_by_week(year, week, category_name)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)
