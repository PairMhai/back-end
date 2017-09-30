from django.contrib import admin
from .models import CreditCard


class CreditCardAdmin(admin.ModelAdmin):
    exclude = ('credit_no', 'ccv')
    readonly_fields = ('id', 'imp_credit_no', 'imp_ccv', 'owner',
                       'expire_date', 'customer')

    def imp_credit_no(self, obj):
        return "**** **** **** " + obj.credit_no[12:16]
    imp_credit_no.short_description = 'Credit Number'

    def imp_ccv(self, obj):
        return "***"
    imp_ccv.short_description = 'CCV'

    class Meta:
        model = CreditCard


admin.site.register(CreditCard, CreditCardAdmin)
