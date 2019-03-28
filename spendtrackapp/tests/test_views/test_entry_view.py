import json

from django.shortcuts import reverse
from freezegun import freeze_time

from spendtrackapp.models.entry import Entry
from spendtrackapp.tests.utils import data_provider
from .provide_data_test_entry import *
from .test_view import *


class TestEntryView(TestView):
    fixtures = ['test/auth_user.json', 'test/entry_categories.json', 'test/category.json', 'test/entry.json']

    @data_provider(entry_add_success)
    def test_add_success(self, time, data, expected_entries_in_week_id, expected_total_in_week):
        with freeze_time(time):
            self.logIn()
            response = self.client.post(reverse('entry:add'), data)
            self.assertEqual(200, response.status_code)
            self.assertTrue('id' in json.loads(response.content.decode('utf-8')))

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

    @data_provider(entry_add_fail)
    def test_add_fail(self, time, data, expected_errors):
        with freeze_time(time):
            self.logIn()
            response = self.client.post(reverse('entry:add'), data)
            self.assertEqual(400, response.status_code)
            errors = json.loads(response.content.decode('utf-8')).keys()
        self.assertEqual(expected_errors, errors)

    @data_provider(entry_edit_success)
    def test_edit_success(self, data):
        response = self.client.post(
            reverse('entry:edit'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data=data
        )
        self.assertEqual(200, response.status_code)

        entry = Entry.objects.get(pk=data['id'])
        self.assertEqual(data['date'], entry.date.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(data['value'], float(entry.value))
        self.assertEqual(data['content'], entry.content)
        self.assertEqual(data['leaf_category'], entry.leaf_category_id)

    @data_provider(entry_edit_fail)
    def test_edit_fail(self, data, errors):
        response = self.client.post(
            reverse('entry:edit'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data=data
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(errors, json.loads(response.content).keys())

    @data_provider(entry_delete_success)
    def test_delete_success(self, entry_id):
        response = self.client.post(
            reverse('entry:delete'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data={'id': entry_id}
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, Entry.objects.filter(id=entry_id).count())

    @data_provider(entry_delete_fail)
    def test_delete_fail(self, entry_id):
        entry_count = Entry.objects.all().count()
        response = self.client.post(
            reverse('entry:delete'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data={'id': entry_id}
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(entry_count, Entry.objects.all().count())
