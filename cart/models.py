from django.db import models


class Order(models.Model):
    total_product = models.IntegerField(default=0)
    final_price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00)
    customer = models.ForeignKey(
        'membership.Customer',
        on_delete=models.CASCADE
    )
    creditcard = models.ForeignKey(
        'payment.CreditCard',
        on_delete=models.CASCADE
    )
    transportation = models.ForeignKey(
        'Transportation',
        on_delete=models.CASCADE
    )
    address = models.TextField(max_length=150, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class OrderInfo(models.Model):
    quantity = models.IntegerField(default=0)
    remarks = models.TextField(max_length=100, default=0)
    order = models.ForeignKey(
        'cart.Order',
        related_name='products',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.id, self.product)


class Transportation(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.name, self.price)
