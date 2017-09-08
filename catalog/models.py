from django.db import models

# Create your models here.
class Design(models.Model):
    """design product v1"""
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2) # max: 999,999.99
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name + " " + self.price

class Material(models.Model):
    """material product v1"""
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2) # max: 999,999.99
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name + " " + self.price

class Pattern(models.Model):
    """pattern of material v1"""
    name = models.CharField(max_length=100)
    primary_color = models.CharField(max_length=100)
    description = models.CharField(max_length=150)

    materials = models.ManyToManyField(Material) # many to many relations

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name + " " + self.description

# no need, since django already provide many to many relations
# class MaterialPattern(models.Model):
#     """weak of material and pattern v1"""
#     material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
#     pattern_id = models.ForeignKey(Pattern, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
