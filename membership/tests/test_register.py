from utils.testcaseutils import MembershipTestCase

from membership.models import Class


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
        response = self.run_create_membership(self.bad_user)
        self.assertResponseCode400(response)

    def test_register_customer(self):
        """if client don't specify class, use default bronze class."""
        self.run_create_membership_and_test(self.good_user)

    def test_info_saved(self):
        """test if customer really stores in the db"""
        self.run_create_membership_and_test(self.good_user)

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
        self.run_create_membership_and_test(self.good_user)  # run and test

        response = self.run_create_membership(
            self.good_user)  # run second time

        self.assertResponseCode400(response)
        self.assertResponseData2(response, "user", "username", [
                                 'A user with that username already exists.'])

    def test_api_autocomplete_class_in_customer(self):
        """if client don't specify class, use default none class."""
        self.run_create_membership(self.good_user)
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
        self.run_create_membership_and_test(self.user_with_class)

        customer = self.get_customer(
            self.user_with_class.get("user").get("username"))
        self.assertEqual(Class.objects.get(
            pk=self.user_with_class.get("classes")), customer.classes)

    def test_register_with_optional_telephone(self):
        telephone = "081-111-1111"
        self.user_with_optional_params.get('user')['telephone'] = telephone

        self.run_create_membership_and_test(self.user_with_optional_params)

        customer = self.get_customer(
            self.user_with_optional_params.get("user").get("username"))
        self.assertEqual(telephone, customer.user.telephone)

    def test_register_with_optional_address(self):
        address = "42 Phaholyothin Road 11100"
        self.user_with_optional_params.get('user')['address'] = address

        self.run_create_membership_and_test(self.user_with_optional_params)

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

        self.run_create_membership_and_test(self.user_with_optional_params)

        customer = self.get_customer(
            self.user_with_optional_params.get("user").get("username"))
        self.assertEqual(year, customer.user.date_of_birth.year)
        self.assertEqual(month, customer.user.date_of_birth.month)
        self.assertEqual(day, customer.user.date_of_birth.day)

    def test_register_with_optional_gender(self):
        gender = "female"
        self.user_with_optional_params.get('user')['gender'] = gender

        self.run_create_membership_and_test(self.user_with_optional_params)

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
        self.run_create_membership_and_test(self.user_with_credit_card)

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

        self.run_create_membership_and_test(self.user_with_credit_card)

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

        response = self.run_create_membership(self.bad_user_wrong_password)
        self.assertResponseCode400(response)
