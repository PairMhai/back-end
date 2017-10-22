from django.test import TestCase

from rest_framework import status


class ImpTestCase(TestCase):
    """Test case implement for testing response of this api"""

    def assertResponseCode(self, response, expected):
        self.assertEqual(response.status_code, expected, msg=response.data)

    def assertResponseData(self, response, key, expected):
        self.assertEqual(response.data.get(key), expected, msg=response.data)

    def assertResponseCode200(self, response):
        self.assertResponseCode(response, status.HTTP_200_OK)

    def assertResponseCode201(self, response):
        self.assertResponseCode(response, status.HTTP_201_CREATED)
