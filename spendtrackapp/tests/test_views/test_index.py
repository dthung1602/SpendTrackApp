import json

from django.shortcuts import reverse
from freezegun import freeze_time

from spendtrackapp.tests.utils import data_provider
from .test_view import *
from .provide_data_test_index import *


class TestIndex(TestView):
    fixtures = ['test/auth_user.json', 'test/info.json',
                'test/entry_categories.json', 'test/category.json', 'test/entry.json']

    @data_provider(index_index_entries_in_week)
    def test_index_entries_in_week(self, time, expected_entries_in_week_ids, expected_total_in_week):
        with freeze_time(time):
            self.logIn()
            response = self.client.get(reverse('home'))

            entry_ids = []
            for entry_page in response.context['entries_pages']:
                entry_ids += [entry.id for entry in entry_page]

            self.assertEqual(200, response.status_code)
            self.assertSequenceEqual(
                expected_entries_in_week_ids,
                entry_ids
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

            response = self.client.get(reverse('home'))
            entry_ids = []
            for entry_page in response.context['entries_pages']:
                entry_ids += [entry.id for entry in entry_page]

            self.assertEqual(200, response.status_code)
            self.assertCountEqual(
                expected_entries_in_week_id,
                entry_ids
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
