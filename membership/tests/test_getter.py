from utils.testcaseutils import ImpTestCase, MembershipTestCase

from membership.models import Class

from utils.methodutils import date_to_str


class GettingTestCase(MembershipTestCase):
    fixtures = ['init_class.yaml', 'init_user.yaml',
                'init_customer.yaml', 'init_creditcard.yaml',
                'init_token.yaml', 'init_email.yaml']


class UserGettingTestCase(GettingTestCase):

    def set_constants(self):
        self.test_user = self.get_user("test_user")
        self.test_token = self.get_token(self.test_user)

        self.superman = self.get_user("superman")
        self.superman_token = self.get_token(self.superman)

    def test_get_complete_data_of_test_user(self):
        """Test if getting user complete return as expected data"""
        response = self.run_get_user_membership_and_test(self.test_token)

        self.assertResponseData(response, 'id',
                                self.test_user.id)
        self.assertResponseData(response, 'first_name',
                                self.test_user.first_name)
        self.assertResponseData(response, 'email_address',
                                self.test_user.get_email_str())
        self.assertResponseData(response, 'telephone',
                                self.test_user.telephone)

    def test_get_complete_data_of_superman(self):
        """Test if getting user complete return as expected data"""
        response = self.run_get_user_membership_and_test(self.superman_token)

        self.assertResponseData(response, 'id',
                                self.superman.id)
        self.assertResponseData(response, 'first_name',
                                self.superman.first_name)
        self.assertResponseData(response, 'email_address',
                                self.superman.get_email_str())
        self.assertResponseData(response, 'telephone',
                                self.superman.telephone)

# ------------------------------------
# ------------------------------------


class CustomerGettingTestCase(GettingTestCase):

    def set_constants(self):
        self.test_user = self.get_customer("test_user")
        self.test_token = self.get_token(self.test_user.user)

        self.superman = self.get_customer("superman")
        self.superman_token = self.get_token(self.superman.user)

    def test_key_of_receive_data_test_user_1(self):
        """Test data that need to send to client (user part)"""
        response = self.run_get_customer_membership_and_test(self.test_token)

        self.assertResponseDictKeyExist(response, 'user', 'id')
        self.assertResponseDictKeyExist(response, 'user', 'username')
        self.assertResponseDictKeyExist(response, 'user', 'first_name')
        self.assertResponseDictKeyExist(response, 'user', 'last_name')
        self.assertResponseDictKeyExist(response, 'user', 'email_address')
        self.assertResponseDictKeyExist(response, 'user', 'age')
        self.assertResponseDictKeyExist(response, 'user', 'address')
        self.assertResponseDictKeyExist(response, 'user', 'gender')
        self.assertResponseDictKeyExist(response, 'user', 'date_of_birth')
        self.assertResponseDictKeyExist(response, 'user', 'telephone')

    def test_key_of_receive_data_test_user_2(self):
        """Test data that need to send to client (classes part)"""
        response = self.run_get_customer_membership_and_test(self.test_token)

        self.assertResponseDictKeyExist(response, 'classes', 'id')
        self.assertResponseDictKeyExist(response, 'classes', 'name')
        self.assertResponseDictKeyExist(response, 'classes', 'price')
        self.assertResponseDictKeyExist(response, 'classes', 'description')

    def test_key_of_receive_data_test_user_3(self):
        """Test data that need to send to client (credit_card part)"""
        response = self.run_get_customer_membership_and_test(self.test_token)

        self.assertResponseDictKeyExist(response, 'creditcards',
                                        'id', many=True)
        self.assertResponseDictKeyExist(response, 'creditcards',
                                        'owner', many=True)
        self.assertResponseDictKeyExist(response, 'creditcards',
                                        'credit_no', many=True)

    def test_receive_data_test_user_1(self):
        """Test data of user age is correctly"""
        response = self.run_get_customer_membership_and_test(self.test_token)

        self.assertResponseDict(
            response, 'user',
            'age',
            self.test_user.user.get_age()
        )

    def test_receive_data_test_user_2(self):
        """Test data of user birthday is correctly"""
        response = self.run_get_customer_membership_and_test(self.test_token)

        self.assertResponseDict(
            response, 'user',
            'date_of_birth',
            date_to_str(self.test_user.user.date_of_birth)
        )

    def test_receive_data_test_user_3(self):
        """Test data of user address is correctly"""
        response = self.run_get_customer_membership_and_test(self.test_token)

        self.assertResponseDict(
            response, 'user',
            'address',
            self.test_user.user.address
        )

    def test_receive_data_test_user_4(self):
        """Test data of user email is correctly"""
        response = self.run_get_customer_membership_and_test(self.test_token)

        self.assertResponseDict(
            response, 'user',
            'email_address',
            self.test_user.user.get_email_str()
        )

    def test_receive_data_superman_1(self):
        """Test data of user age is correctly"""
        response = self.run_get_customer_membership_and_test(
            self.superman_token)

        self.assertResponseDict(
            response, 'user',
            'age',
            self.superman.user.get_age()
        )

    def test_receive_data_superman_2(self):
        """Test data of user birthday is correctly"""
        response = self.run_get_customer_membership_and_test(
            self.superman_token)

        self.assertResponseDict(
            response, 'user',
            'date_of_birth',
            date_to_str(self.superman.user.date_of_birth)
        )

    def test_receive_data_superman_3(self):
        """Test data of user address is correctly"""
        response = self.run_get_customer_membership_and_test(
            self.superman_token)

        self.assertResponseDict(
            response, 'user',
            'address',
            self.superman.user.address
        )

    def test_receive_data_superman_4(self):
        """Test data of user email is correctly"""
        response = self.run_get_customer_membership_and_test(
            self.superman_token)

        self.assertResponseDict(
            response, 'user',
            'email_address',
            self.superman.user.get_email_str()
        )

# ------------------------------------
# ------------------------------------


class ClassGettingTestCase(ImpTestCase):
    fixtures = ['init_class.yaml']

    def set_constants(self):
        self.none = Class.objects.get(id=1)
        self.diamond = Class.objects.get(id=5)

    def test_get_data_1(self):
        """Test if getting information of class (1)"""
        response = self.run_get("membership-class-detail", [self.none.id])
        self.assertResponseCode200(response)

        self.assertResponseData(response, 'id', self.none.id)
        self.assertResponseData(response, 'name', self.none.name)
        self.assertResponseData(response, 'price', self.none.price)

    def test_get_data_2(self):
        """Test if getting information of class (2)"""
        response = self.run_get("membership-class-detail", [self.diamond.id])
        self.assertResponseCode200(response)

        self.assertResponseData(response, 'id', self.diamond.id)
        self.assertResponseData(response, 'name', self.diamond.name)
        self.assertResponseData(response, 'price', self.diamond.price)
