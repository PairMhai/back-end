from django.db import models
import datetime


class CreditCard(models.Model):
    credit_no = models.CharField(max_length=16,unique=True)
    ccv = models.CharField(max_length=4)
    owner = models.CharField(max_length=100)  # name of credit card
    expire_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(
        'membership.Customer',
        related_name='creditcards',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "{}".format(self.owner)
