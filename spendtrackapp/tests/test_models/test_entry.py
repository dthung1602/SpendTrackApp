from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from spendtrackapp.models import Category
from spendtrackapp.tests.test_models.provide_data_test_entry import *
from spendtrackapp.tests.utils import data_provider


class TestEntry(TestCase):
    fixtures = ['test/auth_user.json', 'test/entry_categories.json', 'test/category.json', 'test/entry.json', ]

    @data_provider(entry_change_category_success)
    def test_change_category_success(self, entry_id, category_id, expected_ids):
        entry = Entry.objects.get(pk=entry_id)
        category = Category.objects.get(pk=category_id)
        entry.change_category(category)
        category_ids = [cat.id for cat in entry.categories.all()]
        self.assertCountEqual(expected_ids, category_ids)
        self.assertEqual(category_id, entry.leaf_category.id)
        entry.save()
        category_ids = [cat.id for cat in entry.categories.all()]
        self.assertCountEqual(expected_ids, category_ids)
        self.assertEqual(category_id, entry.leaf_category.id)

    @data_provider(entry_change_category_fail)
    def test_change_category_fail(self, entry_id, category_id):
        with self.assertRaises(ValueError):
            entry = Entry.objects.get(pk=entry_id)
            category = Category.objects.get(pk=category_id)
            entry.change_category(category)

    @data_provider(entry_modify_date)
    def test_modify_date(self, func, date, expected_exception):
        with self.assertRaises(expected_exception):
            func(date)

    @data_provider(entry_leaf_category)
    def test_leaf_category(self, entry_id, expected_category_id):
        entry = Entry.objects.get(pk=entry_id)
        self.assertEqual(expected_category_id, entry.leaf_category.id)

    ##############################################################
    #                       FIND METHODS                         #
    ##############################################################

    @data_provider(entry_find_by_date_range)
    def test_find_by_date_range(self, user_id, start_date, end_date, expected_ids):
        user = User.objects.get(id=user_id)
        entries = Entry.find_by_date_range(user, start_date, end_date)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_year)
    def test_find_by_year(self, user_id, year, expected_ids):
        user = User.objects.get(id=user_id)
        entries = Entry.find_by_year(user, year)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_month)
    def test_find_by_month(self, user_id, year, month, expected_ids):
        user = User.objects.get(id=user_id)
        entries = Entry.find_by_month(user, year, month)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_week)
    def test_find_by_week(self, user_id, year, week, expected_ids):
        user = User.objects.get(id=user_id)
        entries = Entry.find_by_week(user, year, week)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    ##############################################################
    #                 CALCULATE TOTAL METHODS                    #
    ##############################################################

    @data_provider(entry_total_by_date_range)
    def test_total_by_date_range(self, user_id, start_date, end_date, expected_total):
        user = User.objects.get(id=user_id)
        total = Entry.total_by_date_range(user, start_date, end_date)
        self.assertAlmostEqual(expected_total, total, 2)

    @data_provider(entry_total_by_year)
    def test_total_by_year(self, user_id, year, expected_total):
        user = User.objects.get(id=user_id)
        total = Entry.total_by_year(user, year)
        self.assertAlmostEqual(expected_total, total, 2)

    @data_provider(entry_total_by_month)
    def test_total_by_month(self, user_id, year, month, expected_total):
        user = User.objects.get(id=user_id)
        total = Entry.total_by_month(user, year, month)
        self.assertAlmostEqual(expected_total, total, 2)

    @data_provider(entry_total_by_week)
    def test_total_by_week(self, user_id, year, week, expected_total):
        user = User.objects.get(id=user_id)
        total = Entry.total_by_week(user, year, week)
        self.assertAlmostEqual(expected_total, total, 2)

    ##############################################################
    #               FIND METHODS WITH CATEGORY                   #
    ##############################################################

    @data_provider(entry_find_by_date_range_with_category)
    def test_find_by_date_range_with_category(self, user_id, start_date, end_date, category_id, expected_ids):
        user = User.objects.get(id=user_id)
        try:
            category = Category.objects.get(id=category_id)
        except ObjectDoesNotExist:
            entries = Entry.find_by_date_range(user, start_date, end_date, category_id)
            entry_ids = list(entry.id for entry in entries)
            self.assertSequenceEqual([], entry_ids)
            return

        entries = Entry.find_by_date_range(user, start_date, end_date, category.id)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

        entries = Entry.find_by_date_range(user, start_date, end_date, category.name)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

        entries = Entry.find_by_date_range(user, start_date, end_date, category)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_year_with_category)
    def test_find_by_year_with_category(self, user_id, year, category_id, expected_ids):
        user = User.objects.get(id=user_id)
        try:
            category = Category.objects.get(id=category_id)
        except ObjectDoesNotExist:
            entries = Entry.find_by_year(user, year, category_id)
            entry_ids = list(entry.id for entry in entries)
            self.assertSequenceEqual([], entry_ids)
            return

        entries = Entry.find_by_year(user, year, category.id)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

        entries = Entry.find_by_year(user, year, category.name)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

        entries = Entry.find_by_year(user, year, category)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_month_with_category)
    def test_find_by_month_with_category(self, user_id, year, month, category_id, expected_ids):
        user = User.objects.get(id=user_id)
        try:
            category = Category.objects.get(id=category_id)
        except ObjectDoesNotExist:
            entries = Entry.find_by_month(user, year, month, category_id)
            entry_ids = list(entry.id for entry in entries)
            self.assertSequenceEqual([], entry_ids)
            return

        entries = Entry.find_by_month(user, year, month, category.id)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

        entries = Entry.find_by_month(user, year, month, category.name)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

        entries = Entry.find_by_month(user, year, month, category)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_week_with_category)
    def test_find_by_week_with_category(self, user_id, year, week, category_id, expected_ids):
        user = User.objects.get(id=user_id)
        try:
            category = Category.objects.get(id=category_id)
        except ObjectDoesNotExist:
            entries = Entry.find_by_week(user, year, week, category_id)
            entry_ids = list(entry.id for entry in entries)
            self.assertSequenceEqual([], entry_ids)
            return

        entries = Entry.find_by_week(user, year, week, category.id)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

        entries = Entry.find_by_week(user, year, week, category.name)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

        entries = Entry.find_by_week(user, year, week, category)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    ##############################################################
    #                 FIND METHODS WITH LIMIT                    #
    ##############################################################

    @data_provider(entry_find_by_date_range_with_limit)
    def test_find_by_date_range_with_limit(self, user_id, start_date, end_date, limit, expected_ids):
        user = User.objects.get(id=user_id)
        entries = Entry.find_by_date_range(user, start_date, end_date, limit=limit)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_year_with_limit)
    def test_find_by_year_with_limit(self, user_id, year, limit, expected_ids):
        user = User.objects.get(id=user_id)
        entries = Entry.find_by_year(user, year, limit=limit)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_month_with_limit)
    def test_find_by_month_with_limit(self, user_id, year, month, limit, expected_ids):
        user = User.objects.get(id=user_id)
        entries = Entry.find_by_month(user, year, month, limit=limit)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_week_with_limit)
    def test_find_by_week_with_limit(self, user_id, year, week, limit, expected_ids):
        user = User.objects.get(id=user_id)
        entries = Entry.find_by_week(user, year, week, limit=limit)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)
