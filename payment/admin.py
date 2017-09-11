from django.contrib import admin
from .models import BankAccount

class BankAccountAdmin(admin.ModelAdmin):
    class Meta:
        model = BankAccount

admin.site.register(BankAccount, BankAccountAdmin)

