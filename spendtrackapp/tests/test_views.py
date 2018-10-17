import json

from django.contrib.auth import authenticate
from django.shortcuts import reverse
from django.test import TestCase
from freezegun import freeze_time

from .provide_data_views import *
from .utils import data_provider


class TestIndex(TestCase):
    fixtures = ['test/auth_user.json', 'test/info.json',
                'test/entry_categories.json', 'test/category.json', 'test/entry.json']

    def setUp(self):
        user = authenticate(username='dtrump', password='unitedstates')
        self.client.force_login(user)

    @data_provider(index_index_entries_in_week)
    def test_index_entries_in_week(self, time, expected_entries_in_week_ids, expected_total_in_week):
        with freeze_time(time):
            self.setUp()
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

    @data_provider(index_index_others)
    def test_index_others(self, expected_balance, expected_root_categories_ids):
        response = self.client.get(reverse('index'))
        self.assertAlmostEqual(
            expected_balance,
            response.context['current_balance']
        )
        self.assertCountEqual(
            expected_root_categories_ids,
            [cat.id for cat in response.context['root_categories']]
        )

    @data_provider(index_add_success)
    def test_add_success(self, time, data, expected_entries_in_week_id, expected_total_in_week):
        with freeze_time(time):
            self.setUp()
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
            self.setUp()
            response = self.client.post(reverse('add'), data)
            self.assertEqual(400, response.status_code)
            errors = json.loads(response.content.decode('utf-8')).keys()
            self.assertCountEqual(expected_errors, errors)
