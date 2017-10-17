from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from payment.models import CreditCard

# Interesting library
# https://docs.python.org/3/library/doctest.html

# custom user that extend from django auth user


class User(AbstractUser):
    """customer information v1"""
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=13, default="0XX-XXX-XXXX")
    address = models.TextField(default="")
    gender = models.CharField(max_length=20, default="unknown")
    # age = models.IntegerField(default=0)
    date_of_birth = models.DateField(null=True)

    def get_age(self):
        if self.date_of_birth is None:
            return 0
        import datetime
        dob = self.date_of_birth
        tod = datetime.date.today()
        my_age = (tod.year - dob.year) - int((tod.month, tod.day) < (dob.month, dob.day))
        return my_age

    def __str__(self):
        return self.username + ": " + self.first_name + " " + self.last_name


# merge django auth user to customer
class Customer(models.Model):
    """customer information v1"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    classes = models.ForeignKey(
        'Class',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.user)


class Class(models.Model):
    """membership class v1"""
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=3)
    description = models.TextField()

    def __str__(self):
        return self.name
