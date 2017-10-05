import datetime

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse

from django.test import TestCase
from django.test import Client
from random import uniform, randrange

from payment.models import CreditCard
from membership.models import User, Customer, Class


class RegisterTestCase(TestCase):
    fixtures = ['init_class.yaml',
                'init_user.yaml',
                'init_customer.yaml',
                'init_creditcard.yaml',
                'init_token.yaml']

    def __init__(self, *args, **kwargs):
        super(RegisterTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        self.good_creditcard = {
            "customer": "fcf4936b63d9bfa3ebe7f5cf8011517bc6fe8e15",
            "credit_no": "1111111111111111",
            "ccv": "111",
            "owner": "Piromsurang Rookie",
            "expire_date": "2023-06-14"
        }

        self.no_number_creditcard = {
            "customer": "fcf4936b63d9bfa3ebe7f5cf8011517bc6fe8e15",
            "ccv": "111",
            "owner": "Piromsurang Rookie",
            "expire_date": "2023-06-14"
        }

        self.no_ccv_creditcard = {
            "customer": "fcf4936b63d9bfa3ebe7f5cf8011517bc6fe8e15",
            "credit_no": "1111111111111111",
            "owner": "Piromsurang Rookie",
            "expire_date": "2023-06-14"
        }


    def test_if_customer_able_to_create_creditcard(self):
        """test if customer is able to add the new creditcard"""
        response = self.client.post(
            reverse('payment-creator'),
            self.good_creditcard,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_if_no_credicard_number_when_create(self):
        """test if customer is unable to create a new creditcard with missing required params"""
        response = self.client.post(
            reverse('payment-creator'),
            self.no_number_creditcard,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_no_ccv_when_create(self):
        """test if customer is unable to create a new creditcard with missing required params"""
        response = self.client.post(
            reverse('payment-creator'),
            self.no_ccv_creditcard,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
