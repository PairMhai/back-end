from utilities.testcaseutils import MembershipTestCase


class LoginTestCase(MembershipTestCase):

    def set_constants(self):
        self.db_user = self.get_user("test_user")
        self.superman_name = "superman"
        self.superman = {
            "username": self.superman_name,
            "password": "password123"
        }

        self.password_insensitive = {
            "username": "test_user",
            "password": "PasSwOrD123"
        }

        self.username_insensitive = {
            "username": self.db_user.username.upper(),
            "password": "password123"
        }

    def test_login_by_database_user(self):
        """"Test if user can login using database data"""
        data = {
            "username": self.db_user.username,
            "password": "password123"
        }
        response = self.run_login_membership_and_test(data)

        self.assertEqual(self.return_user_id(response), self.db_user.id)

    def test_login_by_raw_data(self):
        """"Test if user can login using raw data"""
        response = self.run_login_membership_and_test(self.superman)

        token_user = self.return_user(response)
        db_user = self.get_user(self.superman_name)
        self.assertEqual(self.superman.get('username'),
                         token_user.username)  # token compare sent data
        # token compare database user
        self.assertEqual(token_user, db_user)

    def test_username_case_sensitive(self):
        """test, username must be case sensitive"""
        response = self.run_login_membership(
            self.username_insensitive)

        self.assertResponseCode400(response)
        self.assertEqual(response.data.get('non_field_errors')[
                         0], "Unable to log in with provided credentials.")

    def test_password_case_sensitive(self):
        """test, password must be case sensitive"""
        response = self.run_login_membership(
            self.password_insensitive)

        self.assertResponseCode400(response)
        self.assertEqual(response.data.get('non_field_errors')[
                         0], "Unable to log in with provided credentials.")


class LoginFailureTestCase(MembershipTestCase):

    def set_constants(self):
        self.baduser_missing_password = {
            "username": "who_are_you"
        }

        self.baduser_missing_username = {
            "password": "password123"
        }

        self.baduser_missing_all = {}

        self.baduser = {
            "username": "who_are_you",
            "password": "password123"
        }

        self.badpassword = {
            "username": "test_user",
            "password": "password1234567890"
        }

    def test_cannot_login_with_unknown_user(self):
        """test, if username is invalid"""
        response = self.run_login_membership(
            self.baduser)
        self.assertResponseCode400(response)
        self.assertEqual(
            response.data.get('non_field_errors')[0],
            "Unable to log in with provided credentials."
        )

    def test_no_parameter(self):
        """test, if don't have body"""
        response = self.run_login_membership(
            self.baduser_missing_all)

        self.assertResponseCode400(response)
        self.assertEqual(
            response.data.get('password')[0],
            "This field is required."
        )

    def test_parameter_username_missing(self):
        """test, if username is missing"""
        response = self.run_login_membership(
            self.baduser_missing_username)

        self.assertResponseCode400(response)
        self.assertEqual(
            response.data.get('non_field_errors')[0],
            "Must include \"username\" and \"password\"."
        )

    def test_parameter_password_missing(self):
        """test, if password is missing"""
        response = self.run_login_membership(
            self.baduser_missing_password)

        self.assertResponseCode400(response)
        self.assertEqual(
            response.data.get('password')[0],
            "This field is required."
        )

    def test_cannot_login_with_wrong_password(self):
        """test, if password is wrong"""
        response = self.run_login_membership(
            self.badpassword)

        self.assertResponseCode400(response)
        self.assertEqual(
            response.data.get('non_field_errors')[0],
            "Unable to log in with provided credentials."
        )
