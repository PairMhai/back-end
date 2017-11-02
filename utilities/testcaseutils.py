from django.test import TestCase
from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APIClient

from membership.models import User, Customer, Class
from rest_framework.authtoken.models import Token


class ImpTestCase(TestCase):
    """Test case implement for testing response of this api"""

    def setUp(self):
        self.pre_setup()
        self.client = APIClient()
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
    fixtures = ['init_class.yaml', 'init_user.yaml', 'init_email.yaml']

    def pre_setup(self):
        from utilities.classes.other import ImpRandomNumber
        self.random_class = ImpRandomNumber()

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
        return Token.objects.get(key=token).user_id

    def get_token(self, user):
        return Token.objects.get(user=user)

    def get_user(self, username):
        return User.objects.get(username=username)

    def get_user_by_id(self, userid):
        return User.objects.get(pk=userid)

    def get_user_by_token(self, token):
        return self.get_user_by_id(self.get_user_id_by_token(token))

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
