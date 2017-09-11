from membership.models import User, Customer, Class
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'firstname', 'lastname', 'email')

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Customer
        fields = ('id', 'user', 'classes')

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('id', 'name', 'price', 'description')
