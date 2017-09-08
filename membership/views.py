from membership.models import Customer, Class
from membership.serializers import CustomerSerializer, ClassSerializer
# from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics

#Create your views here.
class CustomerAction(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ClassDetail(generics.RetrieveAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
