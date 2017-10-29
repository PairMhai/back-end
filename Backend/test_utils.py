from django.test import TestCase

from rest_framework import status

from random import uniform, randrange


class ImpTestCase(TestCase):
    """Test case implement for testing response of this api"""

    def assertResponseCode(self, response, expected):
        self.assertEqual(response.status_code, expected, msg=response.data)

    def assertResponseData(self, response, key, expected):
        self.assertEqual(response.data.get(key), expected, msg=response.data)

    def assertResponseData2(self, response, key1, key2, expected):
        self.assertEqual(response.data.get(key1).get(key2), expected, msg=response.data)

    def assertResponseCode200(self, response):
        self.assertResponseCode(response, status.HTTP_200_OK)

    def assertResponseCode201(self, response):
        self.assertResponseCode(response, status.HTTP_201_CREATED)

    def assertResponseCode400(self, response):
        self.assertResponseCode(response, status.HTTP_400_BAD_REQUEST)


class ImpRandomNumber:

    def random_username(self, title):
        rand_number = str(round(uniform(0, 10000), 5))
        return title + "-" + rand_number

    def random_first_name(self):
        return self.random_username("first")

    def random_last_name(self):
        return self.random_username("last")

    def get_email_of_user(self, username):
        return username + "@test.pairmhai.com"

    def random_email(self):
        username = self.random_username("test-user")
        return username + "@test.pairmhai.com"

    def random_class(self):
        return randrange(1, 7)

    def random_N_digit(self, n):
        """random number with n digit"""
        result = ""
        for _ in range(0, n):
            result += str(int(round(uniform(0, 9), 0)))
        return result

    def random_credit_no(self):
        return self.random_N_digit(16)

    def random_ccv(self):
        return self.random_N_digit(3)

    def random_password(self):
        import uuid
        return uuid.uuid4().hex