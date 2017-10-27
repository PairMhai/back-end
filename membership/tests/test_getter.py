from Backend.test_utils import ImpTestCase

from rest_framework.test import APIClient

from rest_framework import status
from rest_framework.authtoken.models import Token

from django.core.urlresolvers import reverse

from datetime import datetime

from membership.models import User, Customer, Class
from payment.models import CreditCard

def to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()

class UserGettingTestCase(ImpTestCase):
    fixtures = ['init_class.yaml', 'init_user.yaml', 'init_email.yaml', 'init_token.yaml']

    def setUp(self):
        self.test_user = User.objects.get(username='test_user')
        self.test_token = Token.objects.get(user=self.test_user.id)

        self.superman = User.objects.get(username='superman')
        self.superman_token = Token.objects.get(user=self.superman.id)

        self.client = APIClient()
    def test_get_complete_data_of_test_user(self):
        """Test if getting user complete return as expected data"""
        response = self.client.get(
            reverse('membership-user-detail', args=[self.test_token]),
            format="json"
        )
        resp_data = response.data
        self.assertResponseCode200(response)

        self.assertEqual(resp_data.get('id'), self.test_user.id)
        self.assertEqual(resp_data.get('first_name'), self.test_user.first_name)
        self.assertEqual(resp_data.get('email_address'), self.test_user.get_email_str())
        self.assertEqual(resp_data.get('telephone'), self.test_user.telephone)

    def test_get_complete_data_of_superman(self):
        """Test if getting user complete return as expected data"""
        response = self.client.get(
            reverse('membership-user-detail', args=[self.superman_token]),
            format="json"
        )
        resp_data = response.data
        self.assertResponseCode200(response)

        self.assertEqual(resp_data.get('id'), self.superman.id)
        self.assertEqual(resp_data.get('first_name'), self.superman.first_name)
        self.assertEqual(resp_data.get('email_address'), self.superman.get_email_str())
        self.assertEqual(2, len(self.superman.get_emails())) # superman have 2 email
        self.assertEqual(resp_data.get('telephone'), self.superman.telephone)

# ------------------------------------
# ------------------------------------

class CustomerGettingTestCase(ImpTestCase):
    fixtures = ['init_class.yaml', 'init_user.yaml', 'init_customer.yaml', 'init_creditcard.yaml', 'init_token.yaml']

    def setUp(self):
        self.test_user = Customer.objects.get(user=User.objects.get(username='test_user'))
        self.test_token = Token.objects.get(user=self.test_user.user.id)

        self.superman = Customer.objects.get(user=User.objects.get(username='superman'))
        self.superman_token = Token.objects.get(user=self.superman.user.id)
        self.client = APIClient()

    def test_get_complete_data_of_test_user(self):
        """Test if getting customer complete return as expected data"""
        response = self.client.get(
            reverse('membership-cust-detail', args=[self.test_token]),
            format="json"
        )
        resp_data = response.data
        user = resp_data.get('user')
        classes = resp_data.get('classes')
        creditcards = resp_data.get('creditcards')

        self.assertResponseCode200(response)
        self.assertEqual(user['username'], self.test_user.user.username)
        self.assertEqual(user['first_name'], self.test_user.user.first_name)
        self.assertEqual(user['last_name'], self.test_user.user.last_name)
        self.assertEqual(user['age'], self.test_user.user.get_age())
        self.assertEqual(user['telephone'], self.test_user.user.telephone)
        self.assertEqual(to_date(user['date_of_birth']), self.test_user.user.date_of_birth)
        self.assertEqual(user['address'], self.test_user.user.address)
        # must contains class as well
        self.assertEqual(classes['id'], self.test_user.classes.id)
        self.assertEqual(classes['name'], self.test_user.classes.name)
        self.assertEqual(classes['price'], self.test_user.classes.price)
        # must contains payment as well
        db_credits = CreditCard.objects.filter(customer=self.test_user)
        credits = [CreditCard(**creditcards[0]), CreditCard(**creditcards[1])]
        self.assertCountEqual(db_credits, credits)


    def test_get_complete_data_of_superman(self):
        """Test if getting customer complete return as expected data"""
        response = self.client.get(
            reverse('membership-cust-detail', args=[self.superman_token]),
            format="json"
        )
        resp_data = response.data
        user = resp_data.get('user')
        classes = resp_data.get('classes')
        creditcards = resp_data.get('creditcards')

        self.assertResponseCode200(response)
        self.assertEqual(user['username'], self.superman.user.username)
        self.assertEqual(user['first_name'], self.superman.user.first_name)
        self.assertEqual(user['last_name'], self.superman.user.last_name)
        self.assertEqual(user['age'], self.superman.user.get_age())
        self.assertEqual(user['telephone'], self.superman.user.telephone)
        self.assertEqual(to_date(user['date_of_birth']), self.superman.user.date_of_birth)
        self.assertEqual(user['address'], self.superman.user.address)
        # must contains class as well
        self.assertEqual(classes['id'], self.superman.classes.id)
        self.assertEqual(classes['name'], self.superman.classes.name)
        self.assertEqual(classes['price'], self.superman.classes.price)
        # must contains payment as well
        db_credits = CreditCard.objects.filter(customer=self.superman)
        creditcards_obj = []
        for cc in creditcards:
            creditcards_obj.append(CreditCard(**cc))
        self.assertCountEqual(db_credits, creditcards_obj)

# ------------------------------------
# ------------------------------------

class ClassGettingTestCase(ImpTestCase):
    fixtures = ['init_class.yaml']

    def setUp(self):
        self.none = Class.objects.get(id=1)
        self.diamond = Class.objects.get(id=5)

        self.client = APIClient()

    def test_get_data_1(self):
        """Test if getting information of class (1)"""
        response = self.client.get(
            reverse('membership-class-detail', args=[self.none.id]),
            format="json"
        )
        resp_data = response.data

        self.assertResponseCode200(response)

        self.assertEqual(resp_data.get('id'), self.none.id)
        self.assertEqual(resp_data.get('name'), self.none.name)
        self.assertEqual(resp_data.get('price'), self.none.price)

    def test_get_data_2(self):
        """Test if getting information of class (2)"""
        response = self.client.get(
            reverse('membership-class-detail', args=[self.diamond.id]),
            format="json"
        )
        resp_data = response.data

        self.assertResponseCode200(response)

        self.assertEqual(resp_data.get('id'), self.diamond.id)
        self.assertEqual(resp_data.get('name'), self.diamond.name)
        self.assertEqual(resp_data.get('price'), self.diamond.price)
