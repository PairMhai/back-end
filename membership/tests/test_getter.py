from django.test import TestCase

from rest_framework.test import APIClient
from membership.models import User, Customer, Class

from rest_framework import status
from django.core.urlresolvers import reverse

class UserGettingTestCase(TestCase):
    fixtures = ['init_class.yaml', 'init_user.yaml']

    def setUp(self):
        self.test_user = User.objects.get(username='test_user')
        self.superman = User.objects.get(username='superman')

        self.client = APIClient()
    def test_get_complete_data_of_test_user(self):
        """Test if getting user complete return as expected data"""
        response = self.client.get(
            reverse('membership-user-detail', args=[self.test_user.id]),
            format="json"
        )
        resp_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(resp_data.get('id'), self.test_user.id)
        self.assertEqual(resp_data.get('first_name'), self.test_user.first_name)
        self.assertEqual(resp_data.get('email'), self.test_user.email)
        self.assertIsNone(resp_data.get('telephone'), msg="telephone is security information.")

    def test_get_complete_data_of_superman(self):
        """Test if getting user complete return as expected data"""
        response = self.client.get(
            reverse('membership-user-detail', args=[self.superman.id]),
            format="json"
        )
        resp_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(resp_data.get('id'), self.superman.id)
        self.assertEqual(resp_data.get('first_name'), self.superman.first_name)
        self.assertEqual(resp_data.get('email'), self.superman.email)
        self.assertIsNone(resp_data.get('telephone'), msg="telephone is security information.")

# ------------------------------------
# ------------------------------------

class CustomerGettingTestCase(TestCase):
    fixtures = ['init_class.yaml', 'init_user.yaml', 'init_customer.yaml']

    def setUp(self):
        self.test_user = Customer.objects.get(user=User.objects.get(username='test_user'))
        self.superman = Customer.objects.get(user=User.objects.get(username='superman'))
        self.client = APIClient()

    def test_get_complete_data_of_test_user(self):
        """Test if getting customer complete return as expected data"""
        response = self.client.get(
            reverse('membership-cust-detail', args=[self.test_user.id]),
            format="json"
        )
        resp_data = response.data
        user = resp_data.get('user')
        classes = resp_data.get('classes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user['username'], self.test_user.user.username)
        self.assertEqual(user['first_name'], self.test_user.user.first_name)
        self.assertEqual(user['last_name'], self.test_user.user.last_name)
        self.assertEqual(user['age'], self.test_user.user.get_age())
        # all of this shouldn't returned
        with self.assertRaisesMessage(KeyError, 'telephone'):
            user['telephone']
        with self.assertRaisesMessage(KeyError, 'address'):
            user['address']
        with self.assertRaisesMessage(KeyError, 'date_of_birth'):
            user['date_of_birth']
        # must contains class as well
        self.assertEqual(classes['id'], self.test_user.classes.id)
        self.assertEqual(classes['name'], self.test_user.classes.name)
        self.assertEqual(classes['price'], self.test_user.classes.price)

    def test_get_complete_data_of_superman(self):
        """Test if getting customer complete return as expected data"""
        response = self.client.get(
            reverse('membership-cust-detail', args=[self.superman.id]),
            format="json"
        )
        resp_data = response.data
        user = resp_data.get('user')
        classes = resp_data.get('classes')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user['username'], self.superman.user.username)
        self.assertEqual(user['first_name'], self.superman.user.first_name)
        self.assertEqual(user['last_name'], self.superman.user.last_name)
        self.assertEqual(user['age'], self.superman.user.get_age())
        # all of this shouldn't returned
        with self.assertRaisesMessage(KeyError, 'telephone'):
            user['telephone']
        with self.assertRaisesMessage(KeyError, 'address'):
            user['address']
        with self.assertRaisesMessage(KeyError, 'date_of_birth'):
            user['date_of_birth']
        # must contains class as well
        self.assertEqual(classes['id'], self.superman.classes.id)
        self.assertEqual(classes['name'], self.superman.classes.name)
        self.assertEqual(classes['price'], self.superman.classes.price)

# ------------------------------------
# ------------------------------------

class ClassGettingTestCase(TestCase):
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

        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(resp_data.get('id'), self.diamond.id)
        self.assertEqual(resp_data.get('name'), self.diamond.name)
        self.assertEqual(resp_data.get('price'), self.diamond.price)
