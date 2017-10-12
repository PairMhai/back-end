from membership.models import User, Customer, Class
from membership.serializers import FullCustomerSerializer, CustomerSerializer, FullUserSerializer, HalfUserSerializer, ClassSerializer

from rest_framework import generics

from Backend.utils import ImpDetailByTokenView


class CustomerDetail(ImpDetailByTokenView):
    queryset = Customer.objects.all()
    serializer_class = FullCustomerSerializer
    id_str = 'user_id'


class UserDetail(ImpDetailByTokenView):
    queryset = User.objects.all()
    serializer_class = FullUserSerializer


class ClassDetail(generics.RetrieveAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    # example of custom response json format
    # def retrieve(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(self.get_object())
    #     return Response({"successful": True, "data": serializer.data})
