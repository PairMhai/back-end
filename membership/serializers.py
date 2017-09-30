from membership.models import User, Customer, Class
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = ('id', 'name', 'price', 'description')
        read_only = ('id', 'name', 'price', 'description')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class HalfUserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(source='get_age', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'age', 'gender')


class FullUserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(source='get_age', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'address', 'age', 'date_of_birth', 'telephone', 'gender')


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # classes = ClassSerializer()

    class Meta:
        model = Customer
        fields = ('id', 'user') # classes

    def save(self, request):
        raw_data = self.context['request'].data
        user_data = ""
        if (self.context['request'].method == "POST"):
            serializer = FullUserSerializer(
                data=raw_data.pop('user')
            )
            if (serializer.is_valid()):
                user_data = serializer.validated_data
            else:
                raise serializers.ValidationError(
                    serializer.errors)
        else:
            raise serializers.ValidationError('only post method')
            # user_data = validated_data.pop('user')  # get user json

        if ('password1' not in raw_data or 'password2' not in raw_data):
            raise serializers.ValidationError(
                'password1 and password2 is required')
        pass1 = raw_data['password1']
        pass2 = raw_data['password2']
        if (pass1 != pass2):
            raise serializers.ValidationError('password not match')
        user_data.update({'password': make_password(pass1)})
        user = User.objects.create(**user_data)  # create user
        user_class = Class.objects.get(id=1)  # get none class by defaul
        # ser = ClassSerializer(data=dict(user_class))
        # if (ser.is_valid()):
        #     print(ser.validated_data)
        # else:
        #     print(ser.errors)
        if ('classes' in raw_data):
            class_id = raw_data['classes']
            user_class = Class.objects.get(id=class_id)
        customer = Customer.objects.create(
            user=user, classes=user_class)  # create customer
        return user


class FullCustomerSerializer(CustomerSerializer):
    user = HalfUserSerializer()
    classes = ClassSerializer()

    class Meta:
        model = Customer
        fields = ('id', 'user', 'classes')
