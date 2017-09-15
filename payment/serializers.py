from payment.models import BankAccount
from rest_framework import serializers

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ('id', 'owner_name', 'credit_no')
