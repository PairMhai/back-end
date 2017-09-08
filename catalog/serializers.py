# from membership.models import Customer
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'firstname', 'lastname',
                  'email', 'telephone', 'address',
                  'classes', 'created_at', 'updated_at')
