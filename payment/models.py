from django.db import models
from datetime import datetime


class CreditCard(models.Model):
    credit_no = models.CharField(max_length=13)
    ccv = models.CharField(max_length=3)
    owner = models.CharField(max_length=100)  # name of credit card
    expire_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(
        'membership.Customer',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "{} {}".format(self.owner, self.credit_no)
