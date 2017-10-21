"""
database model of django
"""
from django.db import models


class Design(models.Model):
    """design product v1"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00)  # max: 999,999.99
    yard = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00)
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

    def get_color(self):
        return self.material.color

    def get_material_name(self):
        return self.material.name


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


class Image(models.Model):
    """image of the material v2"""
    file_name = models.CharField(max_length=100)
    design = models.ForeignKey(
        'Design',
        related_name='images',
        on_delete=models.CASCADE
    ) # default defImage.jpg
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
        return "Design {} object".format(self.design.id) if self.material == None else "Material {} object".format(self.material.id)

    def get_price(self):
        return self.design.price if self.material == None else self.material.price


class Promotion(models.Model):
    # move to cycle 3
    name = models.CharField(max_length=100)
    image_name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    discount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

