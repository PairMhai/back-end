from cart.models import Order, OrderInfo, Transportation
from cart.serializers import TransportationSerializer, OrderSerializer

from rest_framework import generics, status
from rest_framework.response import Response

from django.forms.models import model_to_dict


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
