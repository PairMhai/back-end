from django.contrib.messages import get_messages
from django.contrib.auth.hashers import make_password

from Backend.test_utils import ImpTestCase
from .test_register import MembershipTestCase

from rest_framework.test import APIClient

from membership.models import User, Customer, Class
from rest_framework.authtoken.models import Token

from rest_framework import status
from django.core.urlresolvers import reverse

from random import uniform, randrange


class LoginTestCase(MembershipTestCase):

    def set_constants(self):
        self.db_user = self.get_user("test_user")
        self.superman_name = "superman"
        self.superman = {
            "username": self.superman_name,
            "password": "password123"
        }

        self.password_insensitive = {
            "username": "test_user",
            "password": "PasSwOrD123"
        }

        self.username_insensitive = {
            "username": self.db_user.username.upper(),
            "password": "password123"
        }

    def test_login_by_database_user(self):
        """"Test if user can login using database data"""
        data = {
            "username": self.db_user.username,
            "password": "password123"
        }

        response = self.client.post(
            reverse('rest_login'),
            data,
            format="json"
        )
        self.assertResponseCode200(response)

        id = Token.objects.get(key=response.data.get('key')).user_id
        self.assertEqual(id, self.db_user.id)
    
    def test_login_by_raw_data(self):
        """"Test if user can login using raw data"""
        response = self.client.post(
            reverse('rest_login'),
            self.superman,
            format="json"
        )
        self.assertResponseCode200(response)

        token_user = self.get_user_by_id(Token.objects.get(key=response.data.get('key')).user_id)
        db_user = self.get_user(self.superman_name)
        self.assertEqual(self.superman.get('username'), token_user.username)  # token compare sent data
        self.assertEqual(token_user, db_user)                                 # token compare database user

    def test_username_case_sensitive(self):
        """test, username must be case sensitive"""
        response = self.client.post(
            reverse('rest_login'),
            self.username_insensitive,
            format="json"
        )
        self.assertResponseCode400(response)
        self.assertEqual(response.data.get('non_field_errors')[0], "Unable to log in with provided credentials.")

    def test_password_case_sensitive(self):
        """test, password must be case sensitive"""
        response = self.client.post(
            reverse('rest_login'),
            self.password_insensitive,
            format="json"
        )
        self.assertResponseCode400(response)
        self.assertEqual(response.data.get('non_field_errors')[0], "Unable to log in with provided credentials.")

class LoginFailureTestCase(MembershipTestCase):

    def set_constants(self):
        self.baduser_missing_password = {
            "username": "who_are_you"
        }

        self.baduser_missing_username = {
            "password": "password123"
        }

        self.baduser_missing_all = {}

        self.baduser = {
            "username": "who_are_you",
            "password": "password123"
        }

        self.badpassword = {
            "username": "test_user",
            "password": "password1234567890"
        }

    def test_cannot_login_with_unknown_user(self):
        """test, if username is invalid"""
        response = self.client.post(
            reverse('rest_login'),
            self.baduser,
            format="json"
        )
        self.assertResponseCode400(response)
        self.assertEqual(response.data.get('non_field_errors')[0], "Unable to log in with provided credentials.")

    def test_no_parameter(self):
        """test, if don't have body"""
        response = self.client.post(
            reverse('rest_login'),
            self.baduser_missing_all,
            format="json"
        )
        self.assertResponseCode400(response)
        self.assertEqual(response.data.get('password')[0], "This field is required.")

    def test_parameter_username_missing(self):
        """test, if username is missing"""
        response = self.client.post(
            reverse('rest_login'),
            self.baduser_missing_username,
            format="json"
        )
        self.assertResponseCode400(response)
        self.assertEqual(response.data.get('non_field_errors')[0], "Must include \"username\" and \"password\".")

    def test_parameter_password_missing(self):
        """test, if password is missing"""
        response = self.client.post(
            reverse('rest_login'),
            self.baduser_missing_password,
            format="json"
        )
        self.assertResponseCode400(response)
        self.assertEqual(response.data.get('password')[0], "This field is required.")

    def test_cannot_login_with_wrong_password(self):
        """test, if password is wrong"""
        response = self.client.post(
            reverse('rest_login'),
            self.badpassword,
            format="json"
        )
        self.assertResponseCode400(response)
        self.assertEqual(response.data.get('non_field_errors')[0], "Unable to log in with provided credentials.")