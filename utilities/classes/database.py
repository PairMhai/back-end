from rest_framework import generics, serializers, status, views, mixins
from rest_framework.response import Response

from rest_framework.authtoken.models import Token

from django.http import Http404
from django.utils import timezone
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

from membership.models import User, Customer

from utilities.methods.database import get_object_or_404, get_user_id_by_token


class TokenView(views.APIView):
    lookup_field = ('token')

    def get_id_name(self):
        if hasattr(self, 'id_key_of_user'):
            return self.id_key_of_user
        elif hasattr(self, 'key_id'):
            return self.key_id
        elif hasattr(self, 'user_id'):
            return self.user_id
        else:
            return 'id'

    
    def get_id(self, token):
        return get_user_id_by_token(token)


    def update_kwargs(self, **kwargs):
        try:
            self.kwargs[self.get_id_name()] = self.get_id(kwargs.get('token'))

            env = self.request._request.environ
            obj = "{}".format(env.get("HOME"))
            msg = "{} {}".format(env.get("REQUEST_METHOD"), env.get("PATH_INFO"))
            LogEntry.objects.log_action(
                self.kwargs[self.get_id_name()], ContentType.objects.get_for_model(User).id, 
                self.kwargs, obj, 1, msg
            )
        except Token.DoesNotExist:
            return Response({"detail": "get individual customer must have token"}, status=status.HTTP_401_UNAUTHORIZED)


    def update_lookup_field(self):
        self.lookup_field = self.get_id_name()


class ImpDetailByTokenView(TokenView, generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        r = self.update_kwargs(**kwargs)
        if r is not None:
            return r
        self.update_lookup_field()
        return self.retrieve(request, *args, **kwargs)


class ImpListByTokenView(TokenView, generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        r = self.update_kwargs(**kwargs)
        if r is not None:
            return r
        self.update_lookup_field()
        return self.list(request, *args, **kwargs)


class ImpUpdateByTokenView(TokenView, generics.UpdateAPIView):
    
    def put(self, request, *args, **kwargs):
        return Response({
            "detail": "Method \"PUT\" not allowed."
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        r = self.update_kwargs(**kwargs)
        if r is not None:
            return r
        self.update_lookup_field()
        return self.partial_update(request, *args, **kwargs)


class ImpDestroyByTokenView(TokenView, generics.DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        r = self.update_kwargs(**kwargs)
        if r is not None:
            return r
        self.update_lookup_field()
        return self.destroy(request, *args, **kwargs)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude_fields = kwargs.pop('exclude_fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if exclude_fields is not None:
            for field_name in exclude_fields:
                self.fields.pop(field_name)


class ThaiDateTimeField(serializers.DateTimeField):

    def to_representation(self, value):
        from django.utils import timezone
        import pytz

        tz = pytz.timezone('Asia/Bangkok')
        value = timezone.localtime(value, timezone=tz)
        return super(ThaiDateTimeField, self).to_representation(value)
