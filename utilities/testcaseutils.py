from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from membership.models import User, Customer, Class
from catalog.models import Product
from cart.models import Transportation

from .methods.database import (get_user_id_by_token,
                               get_token_by_user,
                               get_user_by_username,
                               get_user_by_id,
                               get_user_by_token,
                               get_customer_by_username)

from utilities.classes.other import ImpRandomNumber
from utilities.fixtureutils import UserFixture, CatalogFixture, CartFixture


class ImpTestCase(TestCase):
    """Test case implement for testing response of this api"""

    def __init__(self, *args, **kwargs):
        super(ImpTestCase, self).__init__(*args, **kwargs)

        self.good_response = status.HTTP_200_OK
        self.create_response = status.HTTP_201_CREATED
        self.bad_response = status.HTTP_400_BAD_REQUEST

    def setUp(self):
        self.pre_setup()
        self.client = APIClient()
        self.random_class = ImpRandomNumber()
        self.set_constants()
        self.post_setup()

    def pre_setup(self):
        pass

    def post_setup(self):
        pass

    def set_constants(self):
        print("no implemented yet!")

    def assertResponseCode(self, response, expected):
        self.assertEqual(response.status_code, expected, msg=response.data)

    def assertDict(self, input_dict, key, expected):
        self.assertEqual(input_dict[key], expected)

    def assertDictKeyExist(self, input_dict, key):
        self.assertIn(key, input_dict)        # key in dict
        result = input_dict[key]
        if (isinstance(result, str)):
            self.assertNotEqual(result, "")   # not empty as well
        else:
            self.assertIsNotNone(result)      # not empty as well

    def assertDictKeyNotExist(self, input_dict, key):
        self.assertNotIn(key, input_dict)

    def assertResponseDataKeyExist(self, response, key):
        self.assertDictKeyExist(response.data, key)

    def assertResponseData2KeyExist(self, response, key1, key2):
        self.assertDictKeyExist(response.data.get(key1), key2)

    def assertResponseData(self, response, key, expected):
        self.assertEqual(response.data.get(key), expected, msg=response.data)

    def assertResponseData2(self, response, key1, key2, expected):
        self.assertEqual(
            response.data.get(key1).get(key2),
            expected,
            msg=response.data
        )

    def assertResponseDict(self, response, response_key, dict_key, expected):
        self.assertDict(
            response.data.get(response_key),
            dict_key,
            expected
        )

    def assertResponseDictKeyExist(self, response, response_key, dict_key, many=False):
        if (many):
            _dict = response.data.get(response_key)
            for dic in _dict:
                self.assertDictKeyExist(
                    dic,
                    dict_key
                )
        else:
            self.assertDictKeyExist(
                response.data.get(response_key),
                dict_key
            )

    def assertResponseDictKeyNotExist(self, response, response_key, dict_key, many=False):
        if (many):
            _dict = response.data.get(response_key)
            for dic in _dict:
                self.assertDictKeyNotExist(
                    dic,
                    dict_key
                )
        else:
            self.assertDictKeyNotExist(
                response.data.get(response_key),
                dict_key
            )

    def assertResponseListLength(self, response, key, len_list):
        """ len(response.data.get(key)) == len_list """
        self.assertEqual(
            len(response.data.get(key)),
            len_list,
            msg=response.data
        )

    def assertResponse2ListLength(self, response, key1, key2, len_list):
        """ len(response.data.get(key1).get(key2)) == len_list """
        self.assertEqual(
            len(response.data.get(key1).get(key2)),
            len_list,
            msg=response.data
        )

    def assertResponseErrorDetailList(self, response, number, expected):
        """ response.data.get('detail')[number] == expected """
        self.assertEqual(
            response.data.get('detail')[number],
            expected,
            msg=response.data
        )

    def assertResponseErrorDetailListKey(self, response, number, key, expected):
        """ response.data.get('detail')[number].get(key) == expected """
        self.assertEqual(
            response.data.get('detail')[number].get(key),
            expected,
            msg=response.data
        )

    def assertResponseCode200(self, response):
        self.assertResponseCode(response, status.HTTP_200_OK)

    def assertResponseCode201(self, response):
        self.assertResponseCode(response, status.HTTP_201_CREATED)

    def assertResponseCode400(self, response):
        self.assertResponseCode(response, status.HTTP_400_BAD_REQUEST)

    def run_get(self, reverse_path, args=None):
        return self.client.get(
            reverse(reverse_path, args=args),
            format="json"
        )

    def run_post(self, reverse_path, body):
        return self.client.post(
            reverse(reverse_path),
            body,
            format="json"
        )


class MembershipTestCase(ImpTestCase):
    fixtures = UserFixture.fixtures

    def run_create_membership(self, user):
        return self.run_post("rest_register", user)

    def run_create_membership_and_test(self, user):
        response = self.run_create_membership(user)
        self.assertResponseCode201(response)
        return response

    def run_login_membership(self, body):
        return self.run_post("rest_login", body)

    def run_login_membership_and_test(self, user):
        response = self.run_login_membership(user)
        self.assertResponseCode200(response)
        return response

    def run_get_user_membership(self, token):
        return self.run_get('membership-user-detail', [token])

    def run_get_user_membership_and_test(self, token):
        response = self.run_get_user_membership(token)
        self.assertResponseCode200(response)
        return response

    def run_get_customer_membership(self, token):
        return self.run_get('membership-cust-detail', [token])

    def run_get_customer_membership_and_test(self, token):
        response = self.run_get_customer_membership(token)
        self.assertResponseCode200(response)
        return response

    def return_user_id(self, response):
        """return user id from input response (response must have key 'key')"""
        return self.get_user_id_by_token(response.data.get('key'))

    def return_user(self, response):
        """return user object from input response (response must have key 'key')"""
        return self.get_user_by_id(self.return_user_id(response))

    def get_user_id_by_token(self, token):
        return get_user_id_by_token(token)

    def get_token(self, user):
        return get_token_by_user(user)

    def get_user(self, username):
        return get_user_by_username(username)

    def get_user_by_id(self, userid):
        return get_user_by_id(userid)

    def get_user_by_token(self, token):
        return get_user_by_token(token)

    def get_customer(self, username):
        return get_customer_by_username(username)

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


class MembershipTestUtils:
    """Need `ImpTestCase`"""

    def fix_token(self, user_id):
        return Token.objects.get(user_id=user_id).key

    def random_token(self):
        tokens = []
        for t in Token.objects.all():
            tokens += [t.key]

        return self.random_class.random_element_in_list(tokens)

class CatalogTestCase(ImpTestCase):
    fixtures = CatalogFixture.fixtures

    def random_product(self):
        products = []
        for p in Product.objects.all():
            products += [p]

        return self.random_class.random_element_in_list(products)

class CartTestCase(CatalogTestCase, MembershipTestUtils):
    fixtures = CatalogFixture.fixtures + CartFixture.fixtures

    def run_calculate(self, data, test_code=None):
        """200, 201, 400 -> example of test_code"""
        response = self.run_post('calculate', data)
        if test_code is not None:
            self.assertResponseCode(response, test_code)
        return response

    def gen_buyer_json(self, token):
        return {
            "customer": token
        }

    def gen_product_json(self, pid, quantity):
        return {
            "pid": pid,
            "quantity": quantity
        }

    def random_buyer(self):
        return self.gen_buyer_json(self.random_token())

    def random_trans(self):
        transportations = []
        for p in Transportation.objects.all():
            transportations += [p]

        return self.random_class.random_element_in_list(transportations)
      
    def add_product(self, buyer, product_json):
        if 'products' in buyer:
            buyer['products'] += [product_json]
        else:
            buyer['products'] = [product_json]

    def add_transportation(self, buyer):
        buyer['transportation'] = self.random_trans().id

    def add_valid_product_to_buy(self, buyer, product_id=None, quantity=None):
        """ get buyer from random_buyer """
        p = self.random_product()  # random product
        if quantity is None: 
            quantity = self.random_class.random_range(
                1,
                p.get_quantity()
            )  # random quantity
        self.add_product(
            buyer,
            self.gen_product_json(p.id if product_id is None else product_id, quantity)
        )

    def get_price_from(self, response, title_name):
        return response.data.get(title_name)

    def add_invalid_product_to_buy(self, buyer, wrong_id=False):
        """ add invalid product (This method will return product id) """
        p = self.random_product()            # random product
        self.not_exist_product_id = 123456        # assume that this id will not exist
        # get quantity and plus 2 (wrong quantity)
        large_quantity = p.get_quantity() + 2

        if wrong_id:
            self.add_product(
                buyer,
                self.gen_product_json(
                    self.not_exist_product_id,
                    large_quantity
                )
            )  # add every bad product data
            return self.not_exist_product_id
        else:
            self.add_product(
                buyer,
                self.gen_product_json(
                    p.id,
                    large_quantity
                )
            )
            return p.id
