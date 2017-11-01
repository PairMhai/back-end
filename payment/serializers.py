import datetime

from payment.models import CreditCard

from utilities.classes.database import DynamicFieldsModelSerializer

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from membership.models import Customer, User


class CreditCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreditCard
        fields = ('id', 'owner', 'credit_no')


class FullCreditCardSerializer(DynamicFieldsModelSerializer):
    customer = serializers.CharField(max_length=200)

    class Meta:
        model = CreditCard
        fields = ('id', 'owner', 'credit_no', 'ccv', 'expire_date', 'customer')

    def validate_expire_date(self, value):
        if(datetime.date.today() >= value):
            raise serializers.ValidationError("date must not expired.")
        return value

    def validate_ccv(self, value):
        if(len(value) != 3 and len(value) != 4):
            raise serializers.ValidationError("ccv must be 3 or 4 digit.")
        return value

    def validate_credit_no(self, value):
        if(len(value) != 16):
            raise serializers.ValidationError(
                "credit number must be 16 digit.")
        return value

    def validate_customer(self, value):
        try:
            if (isinstance(value, Customer)):
                return value
            return Customer.objects.get(user=User.objects.get(id=Token.objects.get(key=value).user_id))
        except Token.DoesNotExist:
            raise serializers.ValidationError(
                "customer key must be valid token.")
