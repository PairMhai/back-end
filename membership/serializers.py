from membership.models import Customer, Class
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'firstname', 'lastname',
                  'email', 'classes')

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('id', 'name', 'price', 'description')
