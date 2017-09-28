from django.contrib import admin
from .models import CreditCard

class CreditCardAdmin(admin.ModelAdmin):
    class Meta:
        model = CreditCard

admin.site.register(CreditCard, CreditCardAdmin)
