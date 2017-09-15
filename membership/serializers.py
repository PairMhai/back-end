from membership.models import User, Customer, Class
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class FullUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'address', 'date_of_birth', 'telephone')


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ('id', 'user')

    def create(self, validated_data):
        raw_data = self.context['request'].data
        user_data = ""
        if (self.context['request'].method == "POST"):
            serializer = FullUserSerializer(
                data = raw_data.pop('user')
            )
            if (serializer.is_valid()):
                user_data = serializer.validated_data
            else:
                print("SERIALIZER ERRORS: ", serializer.errors)
                return None
        else:
            user_data = validated_data.pop('user')  # get user json
        user = User.objects.create(**user_data)  # create user
        user_class = Class.objects.get(id=1)  # get bronze class by default
        if ('classes' in raw_data):
            class_id = raw_data['classes']
            user_class = Class.objects.get(id=class_id)
        customer = Customer.objects.create(
            user=user, classes=user_class)  # create customer
        return customer

class FullCustomerSerializer(CustomerSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ('id', 'user', 'classes')

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('id', 'name', 'price', 'description')
