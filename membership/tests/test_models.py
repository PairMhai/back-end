from django.test import TestCase

from membership.models import User, Customer, Class


class UserTestCase(TestCase):
    # Create your tests here.

    def __init__(self, *args, **kwargs):
        super(UserTestCase, self).__init__(*args, **kwargs)
        self.username1 = "test_1"
        self.firstname1 = "first_name_1"
        self.lastname1 = "last_name_1"

    def setUp(self):
        User.objects.create(username=self.username1,
                            firstname=self.firstname1, lastname=self.lastname1)
        User.objects.create(username="test_name_2",
                            firstname="first_name_2", lastname="last_name_2")

    def test_default_telephone(self):
        """Animals that can speak are correctly identified"""
        user1 = User.objects.get(username=self.username1)
        self.assertEqual("0XX-XXX-XXXX", user1.telephone)

    def test_correctly_firstname(self):
        """Animals that can speak are correctly identified"""
        user1 = User.objects.get(username=self.username1)
        self.assertEqual(self.firstname1, user1.firstname)

if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False, buffer=False, catchbreak=False)
