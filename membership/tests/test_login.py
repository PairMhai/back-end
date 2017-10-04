from django.contrib.messages import get_messages
from django.contrib.auth.hashers import make_password

from django.test import TestCase

from rest_framework.test import APIClient
from django.test import Client
from membership.models import User, Customer, Class
from rest_framework.authtoken.models import Token

from rest_framework import status
from django.core.urlresolvers import reverse

from random import uniform, randrange

class LoginTestCase(TestCase):
    fixtures = ['init_class.yaml', 'init_user.yaml']

    def setUp(self):

        self.admin = User.objects.get(username='admin')
        self.test_user = User.objects.get(username='test_user')

        self.client = APIClient()

        number = str(round(uniform(0, 10000), 5))
        self.good_user = {
            "user": {
                "username": "good-user" + number,
                "first_name": "good" + number,
                "last_name": "user",
                "email": "good" + number + "@user.com"
            },
            "password1": "asdf123fdssa",
            "password2": "asdf123fdssa"
        }

    def test_tc_001(self):
        """Test if registed user that is already in db can login"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            reverse('rest_register'),
            self.good_user,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        un = self.good_user.get("user").get("username")
        pw = self.good_user.get("password1")
        response = self.client.login(username=un, password=pw)
        self.assertEqual(response, True)

        self.client.logout()

    def test_tc_002(self):
        """Test if unregisted user cannot login"""

        un = self.good_user.get("user").get("username")
        pw = self.good_user.get("password1")
        response = self.client.login(username=un, password=pw)
        self.assertEqual(response, False)

        self.client.logout()

    def test_tc_003(self):
        """Test with valid username and empty
        invalid password such that login must get failed"""

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            reverse('rest_register'),
            self.good_user,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        un = self.good_user.get("user").get("username")
        response = self.client.login(username=un, password="")
        self.assertEqual(response, False)
        response = self.client.login(username=un, password="dkdkkkkd")
        self.assertEqual(response, False)

        self.client.logout()

    def test_tc_004(self):
        """Test with empty username and empty 
        invalid password and check if login fails"""

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            reverse('rest_register'),
            self.good_user,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.login(username="", password="")
        self.assertEqual(response, False)
        response = self.client.login(username="", password="dkdkkkkd")
        self.assertEqual(response, False)

        self.client.logout()

    def test_tc_005(self):
        """Check if the login function handles case sensitivity"""

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            reverse('rest_register'),
            self.good_user,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        un = self.good_user.get("user").get("username")
        pw = self.good_user.get("password1")
        un = un.upper()
        pw = pw.upper()
        response = self.client.login(username=un, password=pw)
        self.assertEqual(response, False)
        response = self.client.login(username=un, password=pw)
        self.assertEqual(response, False)

        self.client.logout()
