from django.db import models
from django.conf import settings


class BankAccount(models.Model):
    name = models.CharField(max_length=100)
    credit_no = models.CharField(max_length=13)
    ccv = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} {0}".format(self.name, self.credit_no)
