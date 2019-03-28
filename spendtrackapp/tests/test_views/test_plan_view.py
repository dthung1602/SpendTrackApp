import json

from django.shortcuts import reverse
from freezegun import freeze_time

from spendtrackapp.models import Plan
from spendtrackapp.tests.utils import *
from .provide_data_test_plan import *
from .test_view import TestView


class TestPlanView(TestView):
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
            reverse('plan:search'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data=data
        )

        self.assertEqual(200, response.status_code)
        plans_from_json = json.loads(response.content.decode('utf-8'))['plans']
        plan_ids = [plan['id'] for plan in plans_from_json]
        self.assertSequenceEqual(expected_plan_ids, plan_ids)

    @data_provider(plan_test_find_fail)
    # TODO change data
    def test_find_fail(self, data, expect_errors):
        response = self.client.post(
            reverse('plan:search'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data=data
        )
        self.assertEqual(400, response.status_code)
        errors = json.loads(response.content.decode('utf-8')).keys()
        self.assertCountEqual(expect_errors, errors)

    @data_provider(plan_test_add_success)
    def test_add_success(self, time, data, expected_new_plan_id, expected_total):
        with freeze_time(time):
            init_count = int(Plan.objects.all().count())
            response = self.client.post(
                reverse('plan:add'),
                HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                data=data
            )
            count = int(Plan.objects.all().count())
            response_object = json.loads(response.content.decode('utf-8'))
            plan_id = response_object['id']
            plan_total = response_object['total']
            plan = Plan.objects.get(id=expected_new_plan_id)

            self.assertEqual(init_count + 1, count)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(expected_new_plan_id, plan_id)
            self.assertEqual(expected_total, float(plan_total))
            self.assertEqual(expected_total, float(plan.total))

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
    def test_edit_success(self, time, data, expected_total):
        with freeze_time(time):
            init_count = int(Plan.objects.all().count())
            response = self.client.post(
                reverse('plan:edit'),
                HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                data=data
            )
            count = int(Plan.objects.all().count())
            plan = Plan.objects.get(id=data['id'])
            total = float(json.loads(response.content.decode('utf-8'))['total'])

            self.assertEqual(expected_total, total)
            self.assertEqual(init_count, count)
            self.assertEqual(response.status_code, 200)

            for key in ['start_date', 'end_date']:
                self.assertEqual(data[key], getattr(plan, key).strftime("%Y-%m-%d"))
            for key in ['name', 'compare']:
                self.assertEqual(data[key], getattr(plan, key))
            self.assertEqual(data.get('category', None), plan.category_id)
            self.assertAlmostEqual(data['planned_total'], float(plan.planned_total), delta=0.01)

    @data_provider(plan_test_edit_fail)
    # TODO similar to test add fail
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
        errors = list(json.loads(response.content.decode('utf-8')).keys())
        count = int(Plan.objects.all().count())

        self.assertEqual(init_count, count)
        self.assertEqual(response.status_code, 400)
        self.assertSequenceEqual(['id'], errors)
