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
        user_data = ""
        if (self.context['request'].method == "POST"):
            serializer = FullUserSerializer(
                data=self.context['request'].data.pop('user')
            )
            if (serializer.is_valid()):
                user_data = serializer.validated_data
            else:
                print("SERIALIZER ERRORS: ", serializer.errors)
                return None
        else:
            user_data = validated_data.pop('user')  # get user json
        user = User.objects.create(**user_data)  # create user
        class_bronze = Class.objects.get(id=1)  # get bronze class by default
        customer = Customer.objects.create(
            user=user, classes=class_bronze)  # create customer
        return customer


class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = ('id', 'name', 'price', 'description')
