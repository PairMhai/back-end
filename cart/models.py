from django.db import models

from catalog.models import Promotion

# App flow #
# create order without `total_product` and `final_price`
# create each orderinfo
# update `total_product` and `final_price`


class OrderInfo(models.Model):
    quantity = models.IntegerField()
    remarks = models.TextField(max_length=100, default="")
    order = models.ForeignKey(
        'cart.Order',
        related_name='products',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE
    )
    associate_promotion = models.ManyToManyField(Promotion)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "id={}: {}".format(self.id, self.product)

    def get_price(self):
        return self.product.get_price() * self.quantity

    # TODO: cannot get discount price, because no event are saved.
    def get_discount_price(self):
        return self.product.get_price() * self.quantity


class Order(models.Model):
    total_product = models.IntegerField()  # default=0
    final_price = models.DecimalField(
        max_digits=8, decimal_places=2)  # default=0.00
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

    def update_total_product(self):
        self.total_product = len(self.get_orderinfos())

    def get_orderinfos(self):
        return OrderInfo.objects.filter(order=self)

    def get_prices(self):
        full_price = 0
        customer_discount = 0
        total_price = 0
        # product_event_price = 0

        for orderinfo in self.get_orderinfos():
            print(orderinfo.get_price())

        final_price = total_price + self.transportation.price
        return {
            "customer_discount": customer_discount,
            "full_price": full_price,
            "product_event_price": product_event_price,
            "total_price": total_price,
            "transportation_price": self.transportation.price,
            "final_price": final_price
        }

    def update_final_price(self):
        pass

    def save(self, force_insert=False, force_update=False,
             using=None, update_fields=None):
        self.update_total_product()
        # self.update_final_price() # FIXME: might slow
        super().save(force_insert, force_update,
                     using, update_fields)


class Transportation(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.name, self.price)
