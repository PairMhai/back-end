from rest_framework import generics, serializers, status, views, mixins
from rest_framework.response import Response

from rest_framework.authtoken.models import Token

from django.http import Http404
from django.utils import timezone

from membership.models import Customer

from utilities.methods.database import get_object_or_404


class TokenView(views.APIView):
    lookup_field = ('token')

    def get_id_name(self):
        if hasattr(self, 'id_key_of_user'):
            return self.id_key_of_user
        else:
            return 'id'

    def update_kwargs(self, **kwargs):
        try:
            self.kwargs[self.get_id_name()] = Token.objects.get(
                key=kwargs.get('token')).user_id
        except Token.DoesNotExist:
            return Response({"detail": "get individual customer must have token"}, status=status.HTTP_401_UNAUTHORIZED)

    def update_lookup_field(self):
        self.lookup_field = self.get_id_name()


class ImpDetailByTokenView(TokenView, generics.RetrieveAPIView):
    lookup_field = ('token')

    def get(self, request, *args, **kwargs):
        self.update_kwargs(**kwargs)
        self.update_lookup_field()
        return self.retrieve(request, *args, **kwargs)


class ImpListByTokenView(generics.ListAPIView):
    lookup_field = ('token')

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        my_id = self.id_str or 'id'
        self.lookup_field = (my_id)
        filter_kwargs = {self.lookup_field: self.uid}

        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, *args, **kwargs):
        # filter only current customer
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(key=kwargs['token'])
            self.set_id(token)
        except Token.DoesNotExist:
            return Response({"detail": "get individual customer must have token"}, status=status.HTTP_401_UNAUTHORIZED)
        return self.list(request, *args, **kwargs)

    def set_id(self, token):
        self.uid = token.user_id


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
