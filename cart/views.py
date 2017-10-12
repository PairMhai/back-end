from membership.models import Customer
from cart.models import Order, OrderInfo, Transportation
from cart.serializers import TransportationSerializer, OrderSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.forms.models import model_to_dict

from Backend.utils import ImpListByTokenView, get_customer_from_user_id

class TransportationListView(generics.ListAPIView):
    queryset = Transportation.objects.all()
    serializer_class = TransportationSerializer


class OrderCreatorView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        order = Order.objects.get(pk=serializer.data.get('id'))
        tran_serializer = TransportationSerializer(
            data=model_to_dict(order.transportation))
        tran_serializer.is_valid(raise_exception=True)
        return Response({
            'id': order.id,
            'total_price': order.total_price,
            'total_product': order.total_product,
            'transportation': tran_serializer.validated_data,
            'created_at': order.created_at
        }, status=status.HTTP_201_CREATED, headers=headers)

class HistoryView(ImpListByTokenView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    id_str = 'customer_id'

    def set_id(self, token):
        self.uid = get_customer_from_user_id(token.user_id).id

    def get_queryset(self):
        return super(HistoryView, self).get_queryset().filter(customer_id=self.uid)
