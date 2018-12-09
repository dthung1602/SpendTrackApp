from django.test import TestCase

from spendtrackapp.tests.utils import data_provider
from .provide_data_test_info import *


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
