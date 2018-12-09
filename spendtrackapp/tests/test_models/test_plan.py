from django.test import TestCase
from freezegun import freeze_time

from spendtrackapp.models import *
from spendtrackapp.tests.utils import data_provider
from .provide_data_test_plan import *


class TestPlan(TestCase):
    fixtures = ['test/category.json', 'test/plan.json', 'test/plan_entry.json']

    @data_provider(plan_get_current_plans)
    def test_get_current_plans(self, time, expected_plan_ids):
        with freeze_time(time):
            plans = Plan.get_current_plans()
            plan_ids = [plan.id for plan in plans]
            self.assertSequenceEqual(expected_plan_ids, plan_ids)

    @data_provider(plan_get_plans_in_date_range)
    def test_get_plans_in_date_range(self, start_date, end_date, expected_plan_ids):
        plans = Plan.get_plans_in_date_range(start_date, end_date)
        plan_ids = [plan.id for plan in plans]
        self.assertSequenceEqual(expected_plan_ids, plan_ids)

    @data_provider(plan_get_plans_in_year)
    def test_get_plans_in_year(self, year, expected_plan_ids):
        plans = Plan.get_plans_in_year(year)
        plan_ids = [plan.id for plan in plans]
        self.assertSequenceEqual(expected_plan_ids, plan_ids)

    @data_provider(plan_get_plans_in_month)
    def test_get_plans_in_month(self, year, month, expected_plan_ids):
        plans = Plan.get_plans_in_month(year, month)
        plan_ids = [plan.id for plan in plans]
        self.assertSequenceEqual(expected_plan_ids, plan_ids)

    @data_provider(plan_get_plans_in_week)
    def test_get_plans_in_week(self, year, week, expected_plan_ids):
        plans = Plan.get_plans_in_week(year, week)
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
