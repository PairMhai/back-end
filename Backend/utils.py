from django.http import Http404

from rest_framework import generics, serializers, status
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from membership.models import Customer

from django.utils import timezone
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404 as _get_object_or_404


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    """
    Same as Django's standard shortcut, but make sure to also raise 404
    if the filter_kwargs don't match the required types.
    """
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, ValidationError):
        raise Http404


def get_customer_from_user_id(uid):
    return Customer.objects.get(user_id=uid)


def update_all_status_promotions(list_of_promotion):
    from django.utils.timezone import now
    sets = list_of_promotion.filter(start_date__lt=now(), end_date__gt=now())
    for q in sets:
        q.change_status(True)
    return sets.filter(status=True)


def is_between_date(start, end, current):
    from django.utils.dateparse import parse_date

    if isinstance(start, str):
        start = parse_date(start)
    else:
        start = start

    if isinstance(end, str):
        end = parse_date(end)
    else:
        end = end

    if isinstance(current, str):
        current = parse_date(current)
    else:
        current = current

    if start < current < end:
        return True
    return False


class ImpDetailByTokenView(generics.RetrieveAPIView):
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
        if hasattr(self, 'id_str'):
            my_id = self.id_str
        else:
            my_id = 'id'
        self.lookup_field = (my_id)
        filter_kwargs = {self.lookup_field: self.uid}

        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(key=kwargs['token'])
            self.set_id(token)
        except Token.DoesNotExist:
            return Response({"detail": "get individual customer must have token"}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def set_id(self, token):
        self.uid = token.user_id


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
        import pytz

        tz = pytz.timezone('Asia/Bangkok')
        value = timezone.localtime(value, timezone=tz)
        return super(ThaiDateTimeField, self).to_representation(value)


class ImpGithub():
    github = None

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def get_github(self):
        from github import Github
        if self.github is None:
            self.github = Github(self.username, self.password)
        return self.github

    def get_pairmhai(self):
        return self.get_github().get_organization("pairmhai")  # return Organization

    def get_backend(self):
        return self.get_pairmhai().get_repo("Backend")  # return Repository

    def get_rate_limiting(self):
        remain, limit = self.get_github().rate_limiting
        from datetime import datetime

        timestamp = self.get_github().rate_limiting_resettime
        date_time = datetime.fromtimestamp(timestamp)
        real_time = datetime.strftime(date_time, '%d/%m/%Y %H:%M:%S:%f')

        return {
            "rate_remaining": remain,
            "rate_limiting": limit,
            "rate_reset_time": real_time
        }
