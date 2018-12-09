import json

from django.shortcuts import reverse
from freezegun import freeze_time

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
