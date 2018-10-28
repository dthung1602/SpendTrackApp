import json
import sys
from datetime import datetime

from django.contrib.auth import authenticate
from django.shortcuts import reverse
from django.test import TestCase
from freezegun import freeze_time

from .provide_data_views import *
from .utils import data_provider, UnbufferedStream


class TestView(TestCase):
    """Base class for view test cases"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        sys.stdout = UnbufferedStream(sys.stdout)  # disable buffering
        sys.stderr = UnbufferedStream(sys.stderr)  # for stdout and stderr

    def setUp(self):
        self.logIn()  # login before further actions

    def logIn(self):
        """Let self.client login"""
        user = authenticate(username='dtrump', password='unitedstates')
        self.client.force_login(user)


class TestIndex(TestView):
    fixtures = ['test/auth_user.json', 'test/info.json',
                'test/entry_categories.json', 'test/category.json', 'test/entry.json']

    @data_provider(index_index_entries_in_week)
    def test_index_entries_in_week(self, time, expected_entries_in_week_ids, expected_total_in_week):
        with freeze_time(time):
            self.logIn()
            response = self.client.get(reverse('index'))

            self.assertEqual(200, response.status_code)
            self.assertSequenceEqual(
                expected_entries_in_week_ids,
                [entry.id for entry in response.context['entries_in_week']]
            )
            self.assertAlmostEqual(
                expected_total_in_week,
                response.context['total_in_week'],
                2
            )

    @data_provider(index_add_success)
    def test_add_success(self, time, data, expected_entries_in_week_id, expected_total_in_week):
        with freeze_time(time):
            self.logIn()
            response = self.client.post(reverse('add'), data)
            self.assertEqual(200, response.status_code)
            self.assertEqual('{}', response.content.decode('utf-8'))

            response = self.client.get(reverse('index'))
            self.assertEqual(200, response.status_code)
            self.assertCountEqual(
                expected_entries_in_week_id,
                [entry.id for entry in response.context['entries_in_week']]
            )
            self.assertAlmostEqual(
                expected_total_in_week,
                response.context['total_in_week'],
                2
            )

    @data_provider(index_add_fail)
    def test_add_fail(self, time, data, expected_errors):
        with freeze_time(time):
            self.logIn()
            response = self.client.post(reverse('add'), data)
            self.assertEqual(400, response.status_code)
            errors = json.loads(response.content.decode('utf-8')).keys()
            self.assertCountEqual(expected_errors, errors)


class TestSummarize(TestView):
    fixtures = ['test/auth_user.json', 'test/entry_categories.json', 'test/category.json', 'test/entry.json']

    def __test_ajax(self, named_path, expected_dict, **kwargs):
        """
        Helper class to abstract away tests that mock ajax requests
        :param named_path: named path to reverse
        :param expected_dict: expected dictionary after loading from response json string
        :param kwargs: named parameters of the named path
        """
        response = self.client.get(
            reverse(named_path, kwargs=kwargs),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        dict_from_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(expected_dict, dict_from_json)

    @data_provider(summarize_date_range_ajax)
    def test_date_range_ajax(self, start_date, end_date, expected_dict):
        self.__test_ajax(
            'summarize:date_range',
            expected_dict,
            start_date=start_date,
            end_date=end_date
        )

    @data_provider(summarize_year_ajax)
    def test_year_ajax(self, year, expected_dict):
        with freeze_time(datetime(year, 1, 1)):
            self.logIn()
            self.__test_ajax(
                'summarize:year',
                expected_dict,
                year=year
            )
            self.__test_ajax(
                'summarize:this_year',
                expected_dict
            )

    @data_provider(summarize_month_ajax)
    def test_month_ajax(self, year, month, expected_dict):
        with freeze_time(datetime(year, month, 1)):
            self.logIn()
            self.__test_ajax(
                'summarize:month',
                expected_dict,
                year=year,
                month=month
            )
            self.__test_ajax(
                'summarize:this_month',
                expected_dict
            )

    @data_provider(summarize_week_ajax)
    def test_week_ajax(self, year, week, expected_dict):
        date_str = str(year) + " " + str(week) + " 1"
        date = datetime.strptime(date_str, "%G %V %u")
        with freeze_time(date):
            self.logIn()
            self.__test_ajax(
                'summarize:week',
                expected_dict,
                year=year,
                week=week
            )
            self.__test_ajax(
                'summarize:this_week',
                expected_dict
            )

    def __test(self, named_path, expected_context, **kwargs):
        """
        Helper class to abstract away tests that do not make ajax requests
        :param named_path: named path to reverse
        :param expected_context: expected context of the response
        :param kwargs: named parameters of the named path
        """
        response = self.client.get(reverse(named_path, kwargs=kwargs))
        self.assertEqual(200, response.status_code)

        for key in expected_context:
            if key == 'entries':
                entries_ids = [entry.id for entry in response.context['entries']]
                self.assertSequenceEqual(expected_context['entries'], entries_ids)
            else:
                self.assertEqual(expected_context[key], response.context[key])

    @data_provider(summarize_date_range)
    def test_date_range(self, start_date, end_date, expected_dict):
        self.__test(
            'summarize:date_range',
            expected_dict,
            start_date=start_date,
            end_date=end_date
        )

    @data_provider(summarize_year)
    def test_year(self, year, expected_dict):
        with freeze_time(datetime(year, 1, 1)):
            self.logIn()
            self.__test(
                'summarize:year',
                expected_dict,
                year=year
            )
            self.__test(
                'summarize:this_year',
                expected_dict
            )

    @data_provider(summarize_month)
    def test_month(self, year, month, expected_dict):
        with freeze_time(datetime(year, month, 1)):
            self.logIn()
            self.__test(
                'summarize:month',
                expected_dict,
                year=year,
                month=month
            )
            self.__test(
                'summarize:this_month',
                expected_dict
            )

    @data_provider(summarize_week)
    def test_week(self, year, week, expected_dict):
        date_str = str(year) + " " + str(week) + " 1"
        date = datetime.strptime(date_str, "%G %V %u")
        with freeze_time(date):
            self.logIn()
            self.__test(
                'summarize:week',
                expected_dict,
                year=year,
                week=week
            )
            self.__test(
                'summarize:this_week',
                expected_dict
            )
