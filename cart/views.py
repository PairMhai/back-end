from membership.models import Customer
from cart.models import Order, OrderInfo, Transportation
from cart.serializers import TransportationSerializer, OrderSerializer, CalculateOrderSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
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


class OrderCalculateView(APIView):

    def post(self, request, format=None):
        # {
        #     "customer": "fcf4936b63d9bfa3ebe7f5cf8011517bc6fe8e15",
        #     "products": [
        #     	{
        #             "pid": 1,
        #             "quantity": 1
        #         },
        #         {
        #             "pid": 2,
        #             "quantity": 1
        #         },
        #         {
        #             "pid": 1,
        #             "quantity": 1
        #         }
        #     ]
        # }
        serializers = CalculateOrderSerializer(data=request.data)
        if (serializers.is_valid()):
            price = 0
            customer_discount = 0
            final_price = 0

            data = serializers.validated_data
            customer = data.get('customer')
            products = data.get('products')
            for d in products:
                p = d.get('product')
                price += p.get_price()
            customer_discount = price * (customer.classes.discount / 100)
            final_price = price - customer_discount
            return Response({
                "raw_price": price,
                "customer_discount": customer_discount,
                "final_price": final_price
            })
        else:
            return Response({"detail": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)


class HistoryView(ImpListByTokenView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    id_str = 'customer_id'

    def set_id(self, token):
        self.uid = get_customer_from_user_id(token.user_id).id

    def get_queryset(self):
        return super(HistoryView, self).get_queryset().filter(customer_id=self.uid)
