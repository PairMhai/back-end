from django.db import models

# Create your models here.

class Order(models.Model):
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    trans_id = models.ForeignKey(
        'Transportation',
        on_delete=models.CASCADE
    )
    bank_acc_id = models.ForeignKey(
        'payment.BankAccount',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.total

class OrderInfo(models.Model):
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.quantity


class Transportation(models.Model):
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.type + " " + self.price