from utilities.testcaseutils import CartTestCase
from random import uniform, randrange

from cart.models import Order, OrderInfo

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
        self.add_invalid_product_to_buy(self.buyer, wrong_id=False)
        response = self.run_calculate(self.buyer, self.bad_response)
        print(response.data)
        # TODO: add error response to client
