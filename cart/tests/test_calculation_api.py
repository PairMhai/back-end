from utilities.testcaseutils import CartTestCase
from random import uniform, randrange

from cart.models import Order, OrderInfo
from catalog.models import Product

from utilities.fixtureutils import AllFixture


class CalculationApiTestCase(CartTestCase):
    fixtures = AllFixture.fixtures

    def set_constants(self):
        self.buyer = self.random_buyer()

    def test_calculation_correctly(self):
        """test, is calculation can completed"""
        self.add_valid_product_to_buy(self.buyer)
        self.run_calculate(self.buyer, self.good_response)

    def test_calculation_key_valid(self):
        """test, is calculation return data as expected"""
        self.add_valid_product_to_buy(self.buyer)
        self.add_valid_product_to_buy(self.buyer)

        response = self.run_calculate(self.buyer, self.good_response)

        self.assertResponseDataKeyExist(response, 'calculate_id')
        self.assertResponseDataKeyExist(response, 'full_price')
        self.assertResponseDataKeyExist(response, 'customer_discount')
        self.assertResponseDataKeyExist(response, 'event_discount')
        self.assertResponseDataKeyExist(response, 'total_price')

    def test_invalid_customer(self):
        """test, if fake customer try to order"""
        self.buyer = self.gen_buyer_json("fake-token")
        self.add_valid_product_to_buy(self.buyer)

        response = self.run_calculate(self.buyer, self.bad_response)
        self.assertResponseData2(response,
                                 'detail',
                                 'customer',
                                 [
                                     'customer key accept either id or token.'
                                 ])

    def test_invalid_product_id(self):
        """ test. if order invalid product id """
        self.add_invalid_product_to_buy(self.buyer, wrong_id=True)
        response = self.run_calculate(self.buyer, self.bad_response)
        self.assertResponseData2(response,
                                 'detail',
                                 'products',
                                 [{
                                     'pid': [
                                         'Invalid pk "' +
                                         str(self.not_exist_product_id) +
                                         '" - object does not exist.'
                                     ]
                                 }])

    def test_invalid_product_quanity(self):
        """ test. if order out of stock """
        pid = self.add_invalid_product_to_buy(self.buyer, wrong_id=False)
        response = self.run_calculate(self.buyer, self.bad_response)

        self.assertResponseListLength(response, "detail", 1)
        self.assertResponseErrorDetailListKey(response, 0, "id", pid)
        self.assertResponseErrorDetailListKey(
            response, 0, "name",
            Product.objects.get(pk=pid).get_object().name
        )

    def test_multiple_invalid_product_quanity(self):
        """ test. if order out of stock multiple times """
        pid1 = self.add_invalid_product_to_buy(self.buyer, wrong_id=False)
        pid2 = self.add_invalid_product_to_buy(self.buyer, wrong_id=False)
        pid3 = self.add_invalid_product_to_buy(self.buyer, wrong_id=False)

        response = self.run_calculate(self.buyer, self.bad_response)

        self.assertResponseListLength(response, "detail", 3)
        self.assertResponseErrorDetailListKey(
            response, 0, "id",
            pid1
        )
        self.assertResponseErrorDetailListKey(
            response, 0, "name",
            Product.objects.get(pk=pid1).get_object().name
        )

        self.assertResponseErrorDetailListKey(
            response, 2, "id",
            pid3
        )
        self.assertResponseErrorDetailListKey(
            response, 2, "name",
            Product.objects.get(pk=pid3).get_object().name
        )
