from rest_framework import serializers

from cart.models import Order, OrderInfo, Transportation

from membership.serializers import FullCustomerSerializer
from catalog.serializers import ProductSerializer

class OrderInfoSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()

    class Meta:
        model = OrderInfo
        fields = ('product', 'quantity')

class OrderSerializer(serializers.ModelSerializer):
    customer = FullCustomerSerializer()
    infos = OrderInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'infos', 'total_price')

class TransportationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transportation
        fields = ('id', 'type', 'price')
