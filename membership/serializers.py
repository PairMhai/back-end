from membership.models import User, Customer, Class
from rest_framework import serializers

# from test
import pprint
pp = pprint.PrettyPrinter(indent=4)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'address', 'date_of_birth', 'telephone')

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = ('id', 'user', 'classes')

    def create(self, validated_data):
        user_data = validated_data.pop('user') # get user json
        pp.pprint(user_data)
        user = User.objects.create(**user_data) # create user
        # fix class be id 1
        customer = Customer.objects.create(user=user, classes="1") # create customer
        return customer

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('id', 'name', 'price', 'description')
