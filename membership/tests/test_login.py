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

    def test_user_in_db_login(self):
        """Test if user that is already in db can login"""
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

    def test_user_not_in_db_login(self):
        """Test if user that is not in db cannot login"""

        un = self.good_user.get("user").get("username")
        pw = self.good_user.get("password1")
        response = self.client.login(username=un, password=pw)
        self.assertEqual(response, False)

        self.client.logout()
