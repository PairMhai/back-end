import datetime

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse

from django.test import TestCase
from django.test import Client
from random import uniform, randrange

from payment.models import CreditCard

class ModelTestCase(TestCase):
    fixtures = ['init_class.yaml',
                'init_user.yaml',
                'init_customer.yaml',
                'init_creditcard.yaml',
                'init_token.yaml']

    def __init__(self, *args, **kwargs):
        super(ModelTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        self.creditcard = CreditCard.objects.get(pk="1")

    def test_credit_no_is_fixed_length(self):
        """credit card number is only 16 length"""
        self.assertTrue( len(self.creditcard.credit_no) == 16 )

    def test_credit_no_is_all_number(self):
        """each digit of creditcard number must be a number"""
        self.assertTrue( self.creditcard.credit_no.isdigit() )

    def test_ccv_is_fixed_length(self):
        """ccv has either 3 or 4 digits"""
        self.assertTrue( len(self.creditcard.ccv) == 3 or len(self.creditcard.ccv) == 4 )

    def test_ccv_is_all_number(self):
        """each digit of ccv must be a number"""
        self.assertTrue( self.creditcard.ccv.isdigit() )

    def test_expire_date_is_not_today(self):
        """expire date of the credit card must not be this month and this year"""
        exp_date = self.creditcard.expire_date.strftime("%Y-%m")
        now_date = datetime.datetime.now().strftime("%Y-%m")
        self.assertTrue( exp_date > now_date )
