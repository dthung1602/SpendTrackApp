import sys

from django.contrib.auth.models import User
from django.test import TestCase

from spendtrackapp.tests.utils import UnbufferedStream


class TestView(TestCase):
    """Base class for view test cases"""

    default_user_id = 1

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        sys.stdout = UnbufferedStream(sys.stdout)  # disable buffering
        sys.stderr = UnbufferedStream(sys.stderr)  # for stdout and stderr

    def setUp(self):
        self.logIn()  # login before further actions

    def logIn(self):
        """Let self.client login"""
        user = User.objects.get(id=self.default_user_id)
        if user is None:
            raise Exception('Login fails')
        self.client.force_login(user)
