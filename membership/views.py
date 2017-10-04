from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from membership.models import User, Customer, Class
from membership.serializers import FullCustomerSerializer, CustomerSerializer, FullUserSerializer, HalfUserSerializer, ClassSerializer

from rest_framework import generics


# code from `rest_framework/generics.py`
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
# ---------------------------------------


class ImpDetailCustomer(generics.RetrieveAPIView):
    lookup_field = ('token')

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        self.lookup_field = (self.id_str)
        # print("GET", self.id_str, str(self.uid))
        filter_kwargs = {self.lookup_field: self.uid}
        obj = get_object_or_404(queryset, **filter_kwargs)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(key=kwargs['token'])
            self.uid = token.user_id
        except Token.DoesNotExist:
            return Response({"detail": "get individual customer must have token"}, status=status.HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)


class CustomerDetail(ImpDetailCustomer):
    queryset = Customer.objects.all()
    serializer_class = FullCustomerSerializer
    id_str = 'user_id'


class UserDetail(ImpDetailCustomer):
    queryset = User.objects.all()
    serializer_class = FullUserSerializer
    id_str = 'id'


class ClassDetail(generics.RetrieveAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    # example of custom response json format
    # def retrieve(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(self.get_object())
    #     return Response({"successful": True, "data": serializer.data})
