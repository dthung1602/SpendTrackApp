import json

from django.shortcuts import reverse
from freezegun import freeze_time

from spendtrackapp.models import Plan
from spendtrackapp.tests.utils import *
from .provide_data_test_plan import *
from .test_view import TestView


class TestPlan(TestView):
    fixtures = ['test/auth_user.json', 'test/category.json',
                'test/plan.json', 'test/plan_entry.json']

    @data_provider(plan_test_index)
    def test_index(self, date, expected_plan_ids):
        with freeze_time(date):
            self.logIn()

            response = self.client.get(reverse('plan:index'))
            plan_ids = [plan.id for plan in response.context['current_plans']]
            self.assertSequenceEqual(expected_plan_ids, plan_ids)

    @data_provider(plan_test_find_success)
    def test_find_success(self, data, expected_plan_ids):
        response = self.client.post(
            reverse('plan:find'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data=data
        )

        plans_from_json = json.loads(response.content.decode('utf-8'))['plans']
        plan_ids = [plan['id'] for plan in plans_from_json]
        self.assertSequenceEqual(expected_plan_ids, plan_ids)

    @data_provider(plan_test_find_fail)
    def test_find_fail(self, data, fail_reason):
        response = self.client.post(
            reverse('plan:find'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data=data
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(fail_reason, response.content.decode('utf-8'))

    @data_provider(plan_test_add_success)
    def test_add_success(self, time, data, expected_new_plan_id):
        with freeze_time(time):
            init_count = int(Plan.objects.all().count())
            response = self.client.post(
                reverse('plan:add'),
                HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                data=data
            )
            count = int(Plan.objects.all().count())
            plan_id = json.loads(response.content.decode('utf-8'))['id']
            plan = Plan.objects.get(id=expected_new_plan_id)

            self.assertEqual(init_count + 1, count)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(expected_new_plan_id, plan_id)

            for key in ['start_date', 'end_date']:
                self.assertEqual(data[key], getattr(plan, key).strftime("%Y-%m-%d"))
            for key in ['name', 'compare']:
                self.assertEqual(data[key], getattr(plan, key))
            self.assertEqual(data.get('category', None), plan.category_id)
            self.assertAlmostEqual(data['planned_total'], float(plan.planned_total), delta=0.01)

    @data_provider(plan_test_add_fail)
    def test_add_fail(self, time, data, expected_errors):
        with freeze_time(time):
            init_count = int(Plan.objects.all().count())
            response = self.client.post(
                reverse('plan:add'),
                HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                data=data
            )
            count = int(Plan.objects.all().count())

            self.assertEqual(init_count, count)
            self.assertEqual(response.status_code, 400)
            errors = json.loads(response.content.decode('utf-8')).keys()
            self.assertCountEqual(expected_errors, errors)

    @data_provider(plan_test_edit_success)
    def test_edit_success(self, time, data):
        with freeze_time(time):
            init_count = int(Plan.objects.all().count())
            response = self.client.post(
                reverse('plan:edit'),
                HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                data=data
            )
            count = int(Plan.objects.all().count())
            plan = Plan.objects.get(id=data['id'])

            self.assertEqual(init_count, count)
            self.assertEqual(response.status_code, 200)

            for key in ['start_date', 'end_date']:
                self.assertEqual(data[key], getattr(plan, key).strftime("%Y-%m-%d"))
            for key in ['name', 'compare']:
                self.assertEqual(data[key], getattr(plan, key))
            self.assertEqual(data.get('category', None), plan.category_id)
            self.assertAlmostEqual(data['planned_total'], float(plan.planned_total), delta=0.01)

    @data_provider(plan_test_edit_fail)
    # TODO simmilar to test add fail
    def test_edit_fail(self, time, data, expected_errors):
        with freeze_time(time):
            init_count = int(Plan.objects.all().count())
            response = self.client.post(
                reverse('plan:edit'),
                HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                data=data
            )
            count = int(Plan.objects.all().count())
            errors = json.loads(response.content.decode('utf-8')).keys()

            self.assertEqual(init_count, count)
            self.assertEqual(response.status_code, 400)
            self.assertCountEqual(expected_errors, errors)

    @data_provider(plan_test_delete_success)
    def test_delete_success(self, data):
        init_count = int(Plan.objects.all().count())
        response = self.client.post(
            reverse('plan:delete'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data=data
        )
        count = int(Plan.objects.all().count())

        self.assertEqual(init_count, count + 1)
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Plan.DoesNotExist):
            Plan.objects.get(id=data['id'])

    @data_provider(plan_test_delete_fail)
    def test_delete_fail(self, data):
        init_count = int(Plan.objects.all().count())
        response = self.client.post(
            reverse('plan:delete'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data=data
        )
        errors = json.loads(response.content.decode('utf-8')).keys()
        count = int(Plan.objects.all().count())

        self.assertEqual(init_count, count)
        self.assertEqual(response.status_code, 400)
        self.assertSequenceEqual({'id'}, errors)
