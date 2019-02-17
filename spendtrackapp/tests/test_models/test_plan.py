from django.contrib.auth.models import User
from django.test import TestCase
from freezegun import freeze_time

from spendtrackapp.models import Plan
from spendtrackapp.tests.utils import data_provider
from .provide_data_test_plan import *


class TestPlan(TestCase):
    fixtures = ['test/auth_user.json', 'test/category.json', 'test/plan.json', 'test/plan_entry.json']

    @data_provider(plan_get_current_plans)
    def test_get_current_plans(self, user_id, time, expected_plan_ids):
        user = User.objects.get(id=user_id)
        with freeze_time(time):
            plans = Plan.get_current_plans(user)
            plan_ids = [plan.id for plan in plans]
            self.assertSequenceEqual(expected_plan_ids, plan_ids)

    @data_provider(plan_get_plans_in_date_range)
    def test_get_plans_in_date_range(self, user_id, start_date, end_date, expected_plan_ids):
        user = User.objects.get(id=user_id)
        plans = Plan.get_plans_in_date_range(user, start_date, end_date)
        plan_ids = [plan.id for plan in plans]
        self.assertSequenceEqual(expected_plan_ids, plan_ids)

    @data_provider(plan_get_plans_in_year)
    def test_get_plans_in_year(self, user_id, year, expected_plan_ids):
        user = User.objects.get(id=user_id)
        plans = Plan.get_plans_in_year(user, year)
        plan_ids = [plan.id for plan in plans]
        self.assertSequenceEqual(expected_plan_ids, plan_ids)

    @data_provider(plan_get_plans_in_month)
    def test_get_plans_in_month(self, user_id, year, month, expected_plan_ids):
        user = User.objects.get(id=user_id)
        plans = Plan.get_plans_in_month(user, year, month)
        plan_ids = [plan.id for plan in plans]
        self.assertSequenceEqual(expected_plan_ids, plan_ids)

    @data_provider(plan_get_plans_in_week)
    def test_get_plans_in_week(self, user_id, year, week, expected_plan_ids):
        user = User.objects.get(id=user_id)
        plans = Plan.get_plans_in_week(user, year, week)
        plan_ids = [plan.id for plan in plans]
        self.assertSequenceEqual(expected_plan_ids, plan_ids)

    @data_provider(plan_is_completed)
    def test_is_completed(self, plan_id, completed):
        plan = Plan.objects.get(id=plan_id)
        self.assertEqual(completed, plan.is_completed)

    @data_provider(plan_get_entries)
    def test_entries(self, plan_id, expected_entry_ids):
        plan = Plan.objects.get(id=plan_id)

        # test get entries directly
        entry_ids = [entry.id for entry in plan.entries]
        self.assertSequenceEqual(expected_entry_ids, entry_ids)

        # test get entries in cache
        entry_ids = [entry.id for entry in plan.entries]
        self.assertCountEqual(expected_entry_ids, entry_ids)

    @data_provider(plan_total)
    def test_total(self, plan_id, expected_total):
        # test get total directly, without fetching entries
        plan = Plan.objects.get(id=plan_id)
        self.assertEqual(expected_total, plan.total)

        # test get total in cache, without fetching entries
        self.assertEqual(expected_total, plan.total)

        # test get total directly, with entries fetched
        plan = Plan.objects.get(id=plan_id)
        _ = plan.entries
        self.assertEqual(expected_total, plan.total)

        # test get total in cache, with entries fetched
        self.assertEqual(expected_total, plan.total)

    @data_provider(plan_has_passed)
    def test_has_passed(self, time, plan_id, has_passed):
        with freeze_time(time):
            plan = Plan.objects.get(id=plan_id)
            self.assertEqual(has_passed, plan.has_passed)
