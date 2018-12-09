import json
from datetime import datetime

from django.shortcuts import reverse
from freezegun import freeze_time

from spendtrackapp.tests.utils import data_provider
from .test_view import *
from .provide_data_test_summarize import *


class TestSummarize(TestView):
    fixtures = ['test/auth_user.json', 'test/entry_categories.json', 'test/category.json', 'test/entry.json']

    @data_provider(summarize_index_success)
    def test_index_success(self, data, expected_redirected_url):
        response = self.client.post(
            reverse('summarize:index'),
            data=data
        )
        self.assertRedirects(
            response,
            expected_redirected_url,
            status_code=302,
            fetch_redirect_response=False
        )

    @data_provider(summarize_index_fail)
    def test_index_fail(self, data, fail_reason):
        response = self.client.post(
            reverse('summarize:index'),
            data=data
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(fail_reason, response.content.decode('utf-8'))

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

        #  convert all data to float
        for key in dict_from_json:
            if isinstance(dict_from_json[key], list):
                dict_from_json[key] = [float(e) for e in dict_from_json[key]]
            else:
                dict_from_json[key] = float(dict_from_json[key])

        self.assertEqual(200, response.status_code)

        for key in expected_dict:
            self.assertEqual(expected_dict[key], dict_from_json[key])

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
                entries_ids = []
                for entries_page in response.context['entries_pages']:
                    entries_ids += [entry.id for entry in entries_page]
                self.assertSequenceEqual(expected_context['entries'], entries_ids)
            else:
                value = eval(str(response.context[key]))
                self.assertEqual(expected_context[key], value)

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
