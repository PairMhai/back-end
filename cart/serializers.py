from cart.models import Order, OrderInfo, Transportation
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'owner_name', 'credit_no')

class OrderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ('id', 'quantity')

class TransportationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transportation
        fields = ('id', 'type', 'price')
