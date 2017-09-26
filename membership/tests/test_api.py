# https://docs.djangoproject.com/en/1.11/topics/testing/
from django.contrib.messages import get_messages

from django.test import TestCase

from rest_framework.test import APIClient
from django.test import Client
from membership.models import User

from rest_framework import status
from django.core.urlresolvers import reverse

from random import uniform, randrange


class ViewTestCase(TestCase):
    """Test suite for the api views."""
    fixtures = ['init_class.yaml', 'init_user.yaml']

    # (10000 * 99999) - 1 user creatable
    def setUp(self):
        """Define the test client and other test variables."""

        self.admin = User.objects.get(username='admin')
        self.test_user = User.objects.get(username='test_user')

        self.client = APIClient()

        number = str(round(uniform(0, 10000), 5))
        self.bad_user = {
            "user": {
                "username": "bad-user" + number
            }
        }

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

        number = str(round(uniform(0, 10000), 5))
        self.good_user_with_classes = {
            "user": {
                "username": "good-user" + number,
                "first_name": "good" + number,
                "last_name": "user",
                "email": "good" + number + "@user.com"
            },
            "classes": randrange(1, 6),
            "password1": "asdf123fdssa",
            "password2": "asdf123fdssa"
        }

        number = str(round(uniform(0, 10000), 5))
        self.bad_user_with_diff_passwords = {
            "user": {
                "username": "good-user" + number,
                "first_name": "good" + number,
                "last_name": "user",
                "email": "good" + number + "@user.com"
            },
            "classes": randrange(1, 6),
            "password1": "asdf123fdssa",
            "password2": "asdf123fdss1"
        }

    def test_api_bad_request_no_first_last_email(self):
        """firstname lastname and email are required to filled."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            reverse('rest_register'),
            self.bad_user,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()

    # def test_api_auth_403_forbidden(self):
        # """only admin can create new user and customer"""
        # response = self.client.post(
            # reverse('membership'),
            # self.bad_user,
            # format="json"
        # )
        # print(response.data)
        # self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_autocomplete_class_in_customer(self):
        """if client don't specify class, use default bronze class."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            reverse('rest_register'),
            self.good_user,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_api_specify_class_in_customer(self):
        """create customer randomly."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            reverse('rest_register'),
            self.good_user_with_classes,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_api_dismatch_password(self):
        """wrong password cannot login"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            reverse('rest_register'),
            self.bad_user_with_diff_passwords,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()
