import datetime

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse

from payment.models import CreditCard
from membership.models import User, Customer, Class

from utilities.methods.database import get_customer_by_token
from utilities.fixtureutils import MembershipFixture, CreditCardFixture
from utilities.testcaseutils import ImpTestCase


class DestoryTestCase(ImpTestCase):
    fixtures = MembershipFixture.fixtures + CreditCardFixture.fixtures

    def set_constants(self):
        self.token = "fcf4936b63d9bfa3ebe7f5cf8011517bc6fe8e15"
        self.customer = get_customer_by_token(self.token)
        self.creditid = [2, 4]

    def test_delete_able(self):
        """test delete APIs shoud work as expected"""
        before_length = len(self.customer.get_credit_cards())
        response = self.run_delete(
            "payment-delete",
            [
                self.token,
                self.creditid[1]
            ]
        )
        self.assertResponseCode(response, 204)
        after_length = len(self.customer.get_credit_cards())

        self.assertNotEqual(before_length, after_length)
        self.assertEqual(before_length - 1, after_length)

    def test_error_token(self):
        """ token are required to delete credit"""
        response = self.run_delete(
            'payment-delete',
            [
                "wrongtoken",
                self.creditid[1]
            ]
        )
        self.assertResponseCode401(response)

    def test_credit_id_wrong(self):
        response = self.run_delete(
            'payment-delete',
            [
                self.token,
                self.creditid[1] + 1
            ]
        )
        self.assertResponseCode(response, 406) # Not Acceptable
