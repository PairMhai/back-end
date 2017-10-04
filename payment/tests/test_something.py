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


class SomethingTestCase(TestCase):
    fixtures = ['init_class.yaml',
                'init_user.yaml',
                'init_customer.yaml',
                'init_creditcard.yaml',
                'init_token.yaml']

    def __init__(self, *args, **kwargs):
        super(SomethingTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        self.new_creditcard = {
            "customer": "1",
            "credit_no": "1111111111111111",
            "ccv": "111",
            "owner": "Piromsurang Rookie",
            "expire_date": "2023-06-14"
        }


    def test_name(self):
        response = self.client.post(
            reverse('payment-creator'),
            self.new_creditcard,
            format="json"
        )
        print( Customer.objects.all() )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
