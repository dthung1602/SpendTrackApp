from django.test import TestCase

from spendtrackapp.models import *
from spendtrackapp.tests.utils import data_provider
from .provide_data_test_category import *


class TestCategory(TestCase):
    fixtures = ['test/category.json']

    # TODO test create category fail -> exceed max hierarchy depth

    @data_provider(ancestors)
    def test_ancestors(self, category_id, expected_ancestor_ids):
        category = Category.objects.get(pk=category_id)
        ancestor_ids = category.ancestors_ids
        self.assertCountEqual(expected_ancestor_ids, ancestor_ids)

    @data_provider(children)
    def test_children(self, category_id, expected_children_ids):
        category = Category.objects.get(pk=category_id)
        children_id = [child.id for child in category.children]
        self.assertCountEqual(expected_children_ids, children_id)

    @data_provider(is_leaf)
    def test_is_leaf(self, category_id, expected_result):
        category = Category.objects.get(id=category_id)
        self.assertEqual(expected_result, category.is_leaf)

    @data_provider(get_leaf_category)
    def test_get_leaf_category(self, category_id, expected_result):
        category = Category.get_leaf_category(category_id)
        result = category is not None
        self.assertEqual(expected_result, result)

    @data_provider(get_root_categories)
    def test_get_root_categories(self, expected_root_categories_id):
        categories = Category.get_root_categories()
        root_category_ids = [cat.id for cat in categories]
        self.assertEqual(expected_root_categories_id, root_category_ids)
