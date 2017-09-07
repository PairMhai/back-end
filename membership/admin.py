from django.contrib import admin
from .models import Customer, Class

class CustomerAdmin(admin.ModelAdmin):
    class Meta:
        model = Customer

admin.site.register(Customer, CustomerAdmin)

class ClassAdmin(admin.ModelAdmin):
    class Meta:
        model = Class

admin.site.register(Class, ClassAdmin)
