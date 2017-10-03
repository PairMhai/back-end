from cart.models import Order, OrderInfo, Transportation
from cart.serializers import TransportationSerializer
# from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics

#Create your views here.
class TransportationListView(generics.ListAPIView):
    queryset = Transportation.objects.all()
    serializer_class = TransportationSerializer

class TransportationListView(generics.CreateAPIView):
    queryset = Transportation.objects.all()
    serializer_class = TransportationSerializer
