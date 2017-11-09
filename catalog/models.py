"""
database model of django
"""
from django.db import models
from django.utils.timezone import datetime

from utilities.methods.database import update_all_status_promotions
from utilities.methods.other import is_between_date


class Design(models.Model):
    """design product v1"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    # calculate price by material price * yard
    # price = models.DecimalField(
    # max_digits=8, decimal_places=2, default=0.00)  # max: 999,999.99
    yard = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    material = models.ForeignKey(
        'Material',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def get_product_id(self):
        return Product.objects.get(design=self).id

    def get_price(self):
        return self.material.price * self.yard

    def get_quantity(self):
        import math
        return math.floor(self.material.quantity / self.yard)

    def get_discount_price(self):
        sets = self.get_associate_promotion()
        price = self.get_price()
        discount = 0
        for pro in sets:
            discount = price * (pro.discount / 100)
        return price - discount

    def get_associate_promotion(self):
        return update_all_status_promotions(Promotion.objects.all())


class Material(models.Model):
    """material product v1"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)  # description of material
    quantity = models.IntegerField(default=0)  # stock
    price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00)  # max: 999,999.99
    color = models.CharField(max_length=50)  # material color
    image_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_product_id(self):
        return Product.objects.get(material=self).id

    def get_discount_price(self):
        sets = self.get_associate_promotion()
        discount = 0
        for pro in sets:
            discount = self.price * (pro.discount / 100)
        return self.price - discount

    def get_associate_promotion(self):
        return update_all_status_promotions(Promotion.objects.all())


class Image(models.Model):
    """image of the material v2"""
    file_name = models.CharField(max_length=100)
    design = models.ForeignKey(
        'Design',
        related_name='images',
        on_delete=models.CASCADE
    )  # default defImage.jpg
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name


class Product(models.Model):
    design = models.ForeignKey(
        'Design',
        related_name='product',
        null=True,
        on_delete=models.CASCADE
    )
    material = models.ForeignKey(
        'Material',
        related_name='product',
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "Design {} object".format(self.design.id) if self.material is None else "Material {} object".format(self.material.id)

    def get_quantity(self):
        return self.design.get_quantity() if self.material is None else self.material.quantity

    def get_object(self):
        return self.design if self.material is None else self.material

    def get_price(self):
        return self.design.get_price() if self.material is None else self.material.price

    def get_discount_price(self):
        return self.design.get_discount_price() if self.material is None else self.material.get_discount_price()


class Promotion(models.Model):
    # move to cycle 3
    name = models.CharField(max_length=100)
    image_name = models.CharField(max_length=100)
    discount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00)
    status = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True, null=True)
    end_date = models.DateTimeField(auto_now_add=True, null=True)
    description = models.CharField(max_length=150, default=0)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Pro {}".format(self.name)

    def change_status(self, new_status):
        self.status = new_status
        self.save()
        return self.status

    def update_status(self):
        from django.utils.timezone import now

        if self.start_date is None or self.end_date is None:
            return self.status
        # django default timezone (not bangkok timezone)
        today = now()
        if is_between_date(self.start_date, self.end_date, today):
            # print("update status => True")
            self.status = True
        else:
            # print("update status => False")
            self.status = False
        self.save()
        return self.status
