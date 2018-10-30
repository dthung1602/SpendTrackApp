from django.test import TestCase

from spendtrackapp.models import *
from .provide_data_models import *
from .utils import data_provider


class TestCategory(TestCase):
    fixtures = ['test/category.json']

    # TODO test create category fail -> exceed max hierarchy depth

    @data_provider(category_ancestors)
    def test_ancestors(self, category_id, expected_ancestor_ids):
        category = Category.objects.get(pk=category_id)
        ancestor_ids = category.ancestors_ids
        self.assertCountEqual(expected_ancestor_ids, ancestor_ids)

    @data_provider(category_children)
    def test_children(self, category_id, expected_children_ids):
        category = Category.objects.get(pk=category_id)
        children_id = [child.id for child in category.children]
        self.assertCountEqual(expected_children_ids, children_id)

    @data_provider(category_is_leaf)
    def test_is_leaf(self, category_id, expected_result):
        category = Category.objects.get(id=category_id)
        self.assertEqual(expected_result, category.is_leaf)

    @data_provider(category_get_leaf_category)
    def test_get_leaf_category(self, category_id, expected_result):
        category = Category.get_leaf_category(category_id)
        result = category is not None
        self.assertEqual(expected_result, result)

    @data_provider(category_get_root_categories)
    def test_get_root_categories(self, expected_root_categories_id):
        categories = Category.get_root_categories()
        root_category_ids = [cat.id for cat in categories]
        self.assertEqual(expected_root_categories_id, root_category_ids)


class TestEntry(TestCase):
    fixtures = ['test/entry_categories.json', 'test/category.json', 'test/entry.json', ]

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

    ##############################################################
    #                 FIND METHODS WITH LIMIT                    #
    ##############################################################

    @data_provider(entry_find_by_date_range_with_limit)
    def test_find_by_date_range_with_limit(self, start_date, end_date, limit, expected_ids):
        entries = Entry.find_by_date_range(start_date, end_date, limit=limit)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_year_with_limit)
    def test_find_by_year_with_limit(self, year, limit, expected_ids):
        entries = Entry.find_by_year(year, limit=limit)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_month_with_limit)
    def test_find_by_month_with_limit(self, year, month, limit, expected_ids):
        entries = Entry.find_by_month(year, month, limit=limit)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)

    @data_provider(entry_find_by_week_with_limit)
    def test_find_by_week_with_limit(self, year, week, limit, expected_ids):
        entries = Entry.find_by_week(year, week, limit=limit)
        entry_ids = list(entry.id for entry in entries)
        self.assertSequenceEqual(expected_ids, entry_ids)


class TestInfo(TestCase):
    fixtures = ['test/info.json']

    @data_provider(info_get_success)
    def test_get_success(self, name, expected_value, expected_value_type):
        value = Info.get(name).value
        self.assertEqual(expected_value_type, type(value))
        self.assertEqual(expected_value, value)

    @data_provider(info_get_fail)
    def test_get_fail(self, name, exception):
        with self.assertRaises(exception):
            x = Info.get(name).value

    @data_provider(info_set_success)
    def test_set_success(self, name, value):
        info = Info.set(name, value)
        self.assertEqual(value, info.value)
        self.assertEqual(value, Info.get(name).value)

    @data_provider(info_set_fail)
    def test_set_fail(self, name, value, exception):
        with self.assertRaises(exception):
            Info.set(name, value)

    ##############################################################
    #                   OVERRIDDEN OPERATORS                     #
    ##############################################################

    # ------------------------  ADD  -----------------------------

    @data_provider(info_add_built_in_type)
    def test_add_built_in_types(self, name, other, expected_value):
        info = Info.get(name)
        self.assertEqual(expected_value, info + other)
        self.assertEqual(expected_value, other + info)

    @data_provider(info_add_info)
    def test_add_info(self, name, other_name, expected_value):
        info = Info.get(name)
        other = Info.objects.get(name=other_name)
        self.assertEqual(expected_value, info + other)
        self.assertEqual(expected_value, other + info)

    @data_provider(info_iadd_built_in_type)
    def test_iadd_built_in_type(self, name, other, expected_value):
        info = Info.get(name)
        info += other
        self.assertEqual(expected_value, info.value)

    @data_provider(info_iadd_info)
    def test_iadd_built_in_type(self, name, other_name, expected_value):
        info = Info.get(name)
        other = Info.objects.get(name=other_name)
        info += other
        self.assertEqual(expected_value, info.value)

    # TODO add test sub, mul, div
