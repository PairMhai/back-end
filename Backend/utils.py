from django.http import Http404

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from membership.models import Customer

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
        my_id = self.id_str or 'id'
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
