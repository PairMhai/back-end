from cart.models import Order

from utilities.testcaseutils import ImpTestCase, MembershipTestUtils
from utilities.methods.database import get_customer_by_token

from utilities.fixtureutils import AllFixture


class HistoryGetter(ImpTestCase, MembershipTestUtils):
    fixtures = AllFixture.fixtures

    def set_constants(self):
        self.token = self.random_token()
        self.customer = get_customer_by_token(self.token)

        self.response = self.run_get('history-detail', [self.token])
        # print(self.response.data)

        self.orders = Order.objects.filter(customer=self.customer)

    def test_data_key(self):
        for resp_ord in self.response.data:
            self.assertDictKeyExist(resp_ord, 'id')
            self.assertDictKeyExist(resp_ord, 'final_price')
            self.assertDictKeyExist(resp_ord, 'products')
            self.assertDictKeyExist(resp_ord, 'created_at')
            self.assertDictKeyExist(resp_ord, 'updated_at')

    def test_all_order_returned(self):
        self.assertEqual(len(self.response.data), len(self.orders))

    def test_valid_data_from_db(self):
        from utilities.methods.other import date_to_str, str_to_date, change_default_timezone, str_to_datedatetime

        for resp_ord, db_ord in zip(self.response.data, self.orders):
            self.assertEqual(resp_ord.get('id'), db_ord.id)
            self.assertEqual(
                resp_ord.get('final_price'),
                str(db_ord.final_price)
            )
            self.assertEqual(
                str_to_datedatetime(resp_ord.get('created_at')),
                change_default_timezone(db_ord.created_at)
            )
            self.assertEqual(
                str_to_datedatetime(resp_ord.get('updated_at')),
                change_default_timezone(db_ord.updated_at)
            )

    def test_all_orderinfo_returned(self):
        for resp_ord, db_ord in zip(self.response.data, self.orders):
            self.assertEqual(
                len(resp_ord.get('products')),
                len(db_ord.get_orderinfos())
            )

    def test_orderinfo_data_key(self):
        if len(self.response.data) <= 0:
            return
        for resp_info in self.response.data[0].get('products'):
            self.assertDictKeyExist(resp_info, 'product')
            self.assertDictKeyExist(resp_info, 'quantity')

    def test_orderinfo_data_valid(self):
        if len(self.response.data) <= 0:
            return
        for resp_info, db_info in zip(self.response.data[0].get('products'), self.orders[0].get_orderinfos()):
            self.assertDictKeyExist(resp_info.get('product'), 'id')
            self.assertDict(resp_info.get('product'), 'id', db_info.product.id)
            self.assertDict(resp_info, 'quantity', db_info.quantity)
