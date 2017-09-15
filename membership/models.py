from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from payment.models import BankAccount

# Interesting library
# https://docs.python.org/3/library/doctest.html

# custom user that extend from django auth user
class User(AbstractUser):
    """customer information v1"""
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    telephone = models.CharField(max_length=13, default="0XX-XXX-XXXX")
    address = models.TextField(default="")
    date_of_birth = models.DateField(null=True)
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
    bank_account = models.ManyToManyField(BankAccount)  # many to many relations

    def __str__(self):
        return self.user

class Class(models.Model):
    """membership class v1"""
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name
