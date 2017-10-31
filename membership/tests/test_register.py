# https://docs.djangoproject.com/en/1.11/topics/testing/
from django.contrib.messages import get_messages
from django.contrib.auth.hashers import make_password

from rest_framework.test import APIClient
from membership.models import User

from rest_framework import status
from django.core.urlresolvers import reverse

from random import uniform, randrange

from membership.models import User, Customer, Class

from Backend.test_utils import ImpRandomNumber, ImpTestCase


class MembershipTestCase(ImpTestCase):
    fixtures = ['init_class.yaml', 'init_user.yaml', 'init_email.yaml']

    def setUp(self):
        self.client = APIClient()
        self.random_class = ImpRandomNumber()

        self.set_constants()

    def set_constants(self):
        print("no implemented yet!")

    def get_user(self, username):
        return User.objects.get(username=username)

    def get_user_by_id(self, id):
        return User.objects.get(pk=id)

    def get_customer(self, username):
        return Customer.objects.get(user=self.get_user(username))

    def get_default_customer(self):
        password = self.random_class.random_password()
        return {
            "user": {
                "username": self.random_class.random_username("good-user"),
                "first_name": self.random_class.random_first_name(),
                "last_name": self.random_class.random_last_name(),
                "email": self.random_class.random_email()
            },
            "password1": password,
            "password2": password
        }

    def get_default_credit_card(self):
        return {
            "owner": self.random_class.random_username("owner"),
            "credit_no": self.random_class.random_credit_no(),
            "ccv": self.random_class.random_ccv(),
            "expire_date": "2022-02-01"
        }


class SimpleTestCase(MembershipTestCase):
    """Test suite for simple APIs (bad request and good ones)."""

    def set_constants(self):
        """Define the test client and other test variables."""
        self.bad_user = {
            "user": {
                "username": self.random_class.random_username("bad-user")
            }
        }

        self.good_user = self.get_default_customer()

    def test_api_bad_request_no_first_last_email(self):
        """firstname lastname and email are required to filled."""
        response = self.client.post(
            reverse('rest_register'),
            self.bad_user,
            format="json"
        )

        self.assertResponseCode400(response)

    def test_register_customer(self):
        """if client don't specify class, use default bronze class."""
        response = self.client.post(
            reverse('rest_register'),
            self.good_user,
            format="json"
        )

        self.assertResponseCode201(response)

    def test_info_saved(self):
        """test if customer really stores in the db"""
        response = self.client.post(
            reverse('rest_register'),
            self.good_user,
            format="json"
        )
        self.assertResponseCode201(response)

        customer = self.get_customer(
            self.good_user.get("user").get("username"))

        self.assertEqual(customer.user.first_name,
                         self.good_user.get("user").get("first_name"))
        self.assertEqual(customer.user.last_name,
                         self.good_user.get("user").get("last_name"))
        self.assertEqual(customer.user.email,
                         self.good_user.get("user").get("email"))

    def test_cannot_register_two_times(self):
        """test if customer register twist"""
        response = self.client.post(
            reverse('rest_register'),
            self.good_user,
            format="json"
        )
        self.assertResponseCode201(response)

        response = self.client.post(
            reverse('rest_register'),
            self.good_user,
            format="json"
        )
        self.assertResponseCode400(response)
        self.assertResponseData2(response, "user", "username", [
                                 'A user with that username already exists.'])

    def test_api_autocomplete_class_in_customer(self):
        """if client don't specify class, use default none class."""
        response = self.client.post(
            reverse('rest_register'),
            self.good_user,
            format="json"
        )
        self.assertResponseCode201(response)
        customer = self.get_customer(
            self.good_user.get("user").get("username"))

        self.assertEqual(Class.objects.get(pk=1), customer.classes)


class OptionalTestCase(MembershipTestCase):

    def set_constants(self):

        self.user_with_class = self.get_default_customer()
        self.user_with_class['classes'] = self.random_class.random_class()

        self.user_with_optional_params = self.get_default_customer()

    def test_api_specify_class_in_customer(self):
        """create customer randomly."""

        response = self.client.post(
            reverse('rest_register'),
            self.user_with_class,
            format="json"
        )
        self.assertResponseCode201(response)

        customer = self.get_customer(
            self.user_with_class.get("user").get("username"))
        self.assertEqual(Class.objects.get(
            pk=self.user_with_class.get("classes")), customer.classes)

    def test_register_with_optional_telephone(self):
        telephone = "081-111-1111"
        self.user_with_optional_params.get('user')['telephone'] = telephone
        response = self.client.post(
            reverse('rest_register'),
            self.user_with_optional_params,
            format="json"
        )
        self.assertResponseCode201(response)

        customer = self.get_customer(
            self.user_with_optional_params.get("user").get("username"))
        self.assertEqual(telephone, customer.user.telephone)

    def test_register_with_optional_address(self):
        address = "42 Phaholyothin Road 11100"
        self.user_with_optional_params.get('user')['address'] = address
        response = self.client.post(
            reverse('rest_register'),
            self.user_with_optional_params,
            format="json"
        )
        self.assertResponseCode201(response)

        customer = self.get_customer(
            self.user_with_optional_params.get("user").get("username"))
        self.assertEqual(address, customer.user.address)

    def test_register_with_optional_date_of_birth(self):
        year = 1986
        month = 11
        day = 1
        date_of_birth = "{}-{}-{}".format(year, month, day)
        self.user_with_optional_params.get(
            'user')['date_of_birth'] = date_of_birth
        response = self.client.post(
            reverse('rest_register'),
            self.user_with_optional_params,
            format="json"
        )
        self.assertResponseCode201(response)

        customer = self.get_customer(
            self.user_with_optional_params.get("user").get("username"))
        self.assertEqual(year, customer.user.date_of_birth.year)
        self.assertEqual(month, customer.user.date_of_birth.month)
        self.assertEqual(day, customer.user.date_of_birth.day)

    def test_register_with_optional_gender(self):
        gender = "female"
        self.user_with_optional_params.get('user')['gender'] = gender
        response = self.client.post(
            reverse('rest_register'),
            self.user_with_optional_params,
            format="json"
        )
        self.assertResponseCode201(response)

        customer = self.get_customer(
            self.user_with_optional_params.get("user").get("username"))
        self.assertEqual(gender, customer.user.gender)


class CreditOptionalTestCase(MembershipTestCase):

    def set_constants(self):
        self.user_with_credit_card = self.get_default_customer()
        self.user_with_credit_card['credit_cards'] = [
            self.get_default_credit_card(), ]

    def test_register_with_credit_card(self):
        """single credit card"""
        response = self.client.post(
            reverse('rest_register'),
            self.user_with_credit_card,
            format="json"
        )
        self.assertResponseCode201(response)
        customer = self.get_customer(
            self.user_with_credit_card.get("user").get("username"))
        credit_no = customer.get_credit_card(0).credit_no

        credit_cards = self.user_with_credit_card.get("credit_cards")

        self.assertEqual(len(credit_cards), len(
            customer.get_credit_cards()))  # single card
        self.assertEqual(len(customer.get_credit_cards()),
                         1)                  # single card
        self.assertEqual(credit_cards[0].get('credit_no'), credit_no)

    def test_register_with_credit_cards(self):
        """multiple credit card"""
        number = 5
        for _ in range(0, number - 1):
            self.user_with_credit_card[
                'credit_cards'] += [self.get_default_credit_card(), ]

        response = self.client.post(
            reverse('rest_register'),
            self.user_with_credit_card,
            format="json"
        )
        self.assertResponseCode201(response)

        customer = self.get_customer(
            self.user_with_credit_card.get("user").get("username"))

        db_credit_cards = customer.get_credit_cards()
        credit_cards = self.user_with_credit_card.get("credit_cards")

        # equal size
        self.assertEqual(len(db_credit_cards), len(credit_cards))
        self.assertEqual(len(db_credit_cards), number)

        for card, db_card in zip(credit_cards, db_credit_cards):
            self.assertEqual(card.get('credit_no'), db_card.credit_no)


class FailureTestCase(MembershipTestCase):

    def set_constants(self):
        self.bad_user_wrong_password = self.get_default_customer()
        self.bad_user_wrong_password[
            'password2'] = self.random_class.random_password()

    def test_api_dismatch_password(self):
        """wrong password cannot login"""
        response = self.client.post(
            reverse('rest_register'),
            self.bad_user_wrong_password,
            format="json"
        )
        self.assertResponseCode400(response)
