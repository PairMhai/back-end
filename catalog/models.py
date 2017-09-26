"""
database model of django
"""
from django.db import models

class Pattern(models.Model):
    """pattern of material v1"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

# Create your models here.
class Design(models.Model):
    """design product v1"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00) # max: 999,999.99
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Material(models.Model):
    """material product v1"""
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00) # max: 999,999.99
    patterns = models.ManyToManyField(Pattern) # many to many relations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Image(models.Model):
    """image of the material v1"""
    file_name = models.CharField(max_length=50)
    material_id = models.ForeignKey(
        'Material',
        on_delete=models.CASCADE
    )
    # size = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.file_name

