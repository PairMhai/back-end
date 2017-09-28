"""
database model of django
"""
from django.db import models

# class Pattern(models.Model):
#     """pattern of material v1"""
#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=150)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return self.name

# Create your models here.
class Design(models.Model):
    """design product v1"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  # max: 999,999.99
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    material = models.ForeignKey(
        'Material',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Material(models.Model):
    """material product v1"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)  # description of material
    quantity = models.IntegerField(default=0)  # stock
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  # max: 999,999.99
    color = models.CharField(max_length=50)  # material color
    image_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    """image of the material v1"""
    file_name = models.CharField(max_length=100)
    design = models.ForeignKey(
        'Design',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name


class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    design = models.ForeignKey(
        'Design',
        on_delete=models.CASCADE
    )
    material = models.ForeignKey(
        'Material',
        on_delete=models.CASCADE
    )


# move to cycle 3
class Promotion(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE
    )
