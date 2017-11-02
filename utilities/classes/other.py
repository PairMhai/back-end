from random import uniform, randrange, choice


class ImpRandomNumber:

    def random_element_in_list(self, input_list):
        return choice(input_list)

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

    def random_range(self, start, end):
        return int(round(uniform(start, end), 0))

    def random_N_digit(self, n):
        """random number with n digit"""
        result = ""
        for _ in range(0, n):
            result += str(self.random_range(0, 9))
        return result

    def random_credit_no(self):
        return self.random_N_digit(16)

    def random_ccv(self):
        return self.random_N_digit(3)

    def random_password(self):
        import uuid
        return uuid.uuid4().hex
