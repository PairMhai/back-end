from membership.models import User, Customer, Class

from payment.models import CreditCard
from payment.serializers import CreditCardSerializer, FullCreditCardSerializer

from allauth.account.models import EmailAddress

from payment.serializers import CreditCardSerializer, FullCreditCardSerializer

from membership.forms import PasswordResetForm

from rest_auth.serializers import (
    LoginSerializer as DefaultLoginSerializer,
    PasswordResetSerializer as DefaultPasswordResetSerializer
)

from rest_framework import serializers, exceptions
from rest_framework.exceptions import ( 
    APIException, 
    NotAcceptable
)

from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from django.db.utils import IntegrityError

UserModel = get_user_model()


class ClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = Class
        fields = ('id', 'name', 'price', 'description')
        read_only = ('id', 'name', 'price', 'description')


class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailAddress
        fields = ('email', 'primary', 'verified')


class UserSerializer(serializers.ModelSerializer):
    email_address = serializers.EmailField(
        source="get_email_str", read_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'email_address')


class HalfUserSerializer(UserSerializer):
    age = serializers.IntegerField(source='get_age', read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('age', 'gender')


class FullUserSerializer(HalfUserSerializer):

    class Meta(HalfUserSerializer.Meta):
        fields = HalfUserSerializer.Meta.fields + \
            ('address', 'date_of_birth', 'telephone')


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ('id', 'user')  # classes

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

        # password check
        if ('password1' not in raw_data or 'password2' not in raw_data):
            raise serializers.ValidationError(
                'password1 and password2 is required')
        pass1 = raw_data['password1']
        pass2 = raw_data['password2']
        if (pass1 != pass2):
            raise serializers.ValidationError('password not match')
        user_data.update({'password': make_password(pass1)})

        try:
            user = User(**user_data)  # create user
            user.save()
            user.set_email(user_data.get('email'))
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        user_class = Class.objects.get(id=1)  # get none class by defaul
        if ('classes' in raw_data):
            class_id = raw_data['classes']
            user_class = Class.objects.get(id=class_id)
        # customer
        customer = Customer.objects.create(
            user=user, classes=user_class)  # create customer
        # credit card
        if ('credit_cards' in raw_data):
            cc_json = raw_data['credit_cards']
            for cc in cc_json:
                # cc.update({'customer': customer})
                s = FullCreditCardSerializer(
                    data=cc, exclude_fields=['customer'])
                if (s.is_valid()):
                    data = s.validated_data
                    data.update({'customer': customer})
                    CreditCard.objects.create(**data)
                else:
                    raise serializers.ValidationError(s.errors)
        return user  # customer


class FullCustomerSerializer(CustomerSerializer):
    user = FullUserSerializer()
    classes = ClassSerializer()
    creditcards = CreditCardSerializer(many=True)

    class Meta:
        model = Customer
        fields = ('id', 'user', 'classes', 'creditcards')


class LoginSerializer(DefaultLoginSerializer):

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

            # Authentication through username
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(
                        email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

            if username:
                user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            from allauth.account.models import EmailAddress

            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                # EmailAddress new implementation
                email = EmailAddress.objects.filter(
                    user_id=user.id, verified=True, primary=True)
                if len(email) == 0:
                    raise serializers.ValidationError(
                        _('E-mail is not verified.'))

        attrs['user'] = user
        LogEntry.objects.log_action(
            user_id=user.id,
            content_type_id=ContentType.objects.get_for_model(User).id,
            object_id=user.id,
            object_repr=repr(user),
            action_flag=1,
            change_message="login"
        )
        return attrs


class PasswordResetSerializer(DefaultPasswordResetSerializer):
    password_reset_form_class = PasswordResetForm

    def save(self):
        try:
            super(PasswordResetSerializer, self).save()
        except ValidationError as e:
            raise NotAcceptable(e.messages[0])
