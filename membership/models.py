from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# custom user that extend from django auth user
class User(AbstractUser):
    """customer information v1"""
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    telephone = models.CharField(max_length=13, default="0XX-XXX-XXXX")
    address = models.TextField(default="")
    date_of_birth = models.DateField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username + ": " + self.firstname + " " + self.lastname

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
        return self.user

# merge django auth user to customer
class Admin(models.Model):
    """customer information v1"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    user.is_staff = True
    classes = models.ForeignKey(
        'Class',
        on_delete=models.CASCADE
    )
    def __str__(self):
        return self.user

class Class(models.Model):
    """membership class v1"""
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    def __str__(self):
        return self.name
