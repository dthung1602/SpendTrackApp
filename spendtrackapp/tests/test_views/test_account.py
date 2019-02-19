import json
import re
from urllib.parse import urlparse

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from spendtrackapp.tests.test_views.provide_data_test_account import *
from spendtrackapp.tests.test_views.test_view import TestView
from spendtrackapp.tests.utils import *


class TestAccountNoLogin(TestCase):
    fixtures = ['test/auth_user.json']

    @data_provider(provide_data_test_register_success)
    def test_register_success(self, data):
        response = self.client.post(
            reverse('account:register'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data=data
        )
        self.assertEqual(302, response.status_code)

    @data_provider(provide_data_test_register_fail)
    def test_register_fail(self, data, errors):
        response = self.client.post(
            reverse('account:register'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data=data
        )
        self.assertEqual(200, response.status_code)
        self.assertSetEqual(set(response.context['errors'].keys()), errors)

    @data_provider(provide_data_test_reset_password)
    def test_password_reset(self, email, username):
        number_of_old_email = len(mail.outbox)

        response = self.client.post(
            reverse('account:password_reset'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data={'email': email}
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(mail.outbox) - number_of_old_email)

        response = self.client.post(
            reverse('account:password_reset'),
            data={'email': email}
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(mail.outbox) - number_of_old_email)

        link_re = re.compile("https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

        link1 = link_re.findall(mail.outbox[number_of_old_email].body)[0]
        link2 = link_re.findall(mail.outbox[number_of_old_email + 1].body)[0]

        self.assertEqual(link1, link2)

        response = self.client.get(urlparse(link1).path)
        self.assertEqual(200, response.status_code)

        user = authenticate(username=username, password=response.context['old_password'])
        self.assertIsNotNone(user)


class TestAccountWithLogin(TestView):
    fixtures = ['test/auth_user.json']

    @data_provider(provide_data_test_edit_account_success)
    def test_edit_account_success(self, data):
        response = self.client.post(
            reverse('account:edit'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data=data
        )
        self.assertEqual(200, response.status_code)

        user = User.objects.get(id=self.default_user_id)
        for k, v in data.items():
            self.assertEqual(v, getattr(user, k))

    @data_provider(provide_data_test_edit_account_fail)
    def test_edit_account_fail(self, data, errors):
        response = self.client.post(
            reverse('account:edit'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data=data
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(errors, json.loads(response.content).keys())

    @data_provider(provide_data_test_delete_account)
    def test_delete_account(self, user_id):
        user = User.objects.get(id=user_id)
        self.client.force_login(user)
        response = self.client.post(
            reverse('account:delete')
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, User.objects.filter(id=user_id).count())

    @data_provider(provide_data_test_password_change_success)
    def test_password_change_success(self, data):
        response = self.client.post(
            reverse('account:password_change'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data=data
        )
        self.assertEqual(200, response.status_code)

        username = User.objects.get(id=self.default_user_id).username
        user = authenticate(username=username, password=data['new_password1'])
        self.assertIsNotNone(user)

    @data_provider(provide_data_test_password_change_fail)
    def test_password_change_fail(self, data, errors):
        response = self.client.post(
            reverse('account:password_change'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            data=data
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual(errors, json.loads(response.content).keys())
