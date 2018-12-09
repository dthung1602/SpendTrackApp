import sys

from django.contrib.auth import authenticate
from django.test import TestCase

from spendtrackapp.tests.utils import UnbufferedStream


class TestView(TestCase):
    """Base class for view test cases"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        sys.stdout = UnbufferedStream(sys.stdout)  # disable buffering
        sys.stderr = UnbufferedStream(sys.stderr)  # for stdout and stderr

    def setUp(self):
        self.logIn()  # login before further actions

    def logIn(self):
        """Let self.client login"""
        user = authenticate(username='dtrump', password='unitedstates')
        self.client.force_login(user)
