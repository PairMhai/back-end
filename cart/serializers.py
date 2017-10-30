from rest_framework import serializers

from rest_framework.authtoken.models import Token
from cart.models import Order, OrderInfo, Transportation
from catalog.models import Product
from membership.models import Customer
from payment.models import CreditCard

from membership.serializers import FullCustomerSerializer
from catalog.serializers import ProductSerializer, ProductDetailSerializer


class OrderInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    pid = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = OrderInfo
        fields = ('product', 'pid', 'quantity')

class OrderInfoDetailSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer(read_only=True)
    pid = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = OrderInfo
        fields = ('product', 'pid', 'quantity')

class CalculateOrderSerializer(serializers.Serializer):
    customer = serializers.CharField(max_length=200)
    products = OrderInfoSerializer(many=True)

    def validate_customer(self, value):
        try:
            return Customer.objects.get(id=Token.objects.get(key=value).user_id)
        except Token.DoesNotExist:
            raise serializers.ValidationError(
                "customer key accept either id or token.")


class OrderCreateSerializer(serializers.ModelSerializer):
    products = OrderInfoSerializer(many=True)

    class Meta:
        model = Order
        fields = ('products', 'total_product', 'final_price',
                  'customer', 'creditcard', 'transportation')

    def create(self, validated_data):
        orders_info = validated_data.pop('products')
        validated_data.update({'total_product': len(orders_info)})
        order = Order.objects.create(**validated_data)
        for info in orders_info:
            info.update({'order': order})
            OrderInfo.objects.create(**info)
        order.final_price += order.transportation.price
        order.save()
        return order


class OrderSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(max_length=100)
    creditcard = serializers.PrimaryKeyRelatedField(
        queryset=CreditCard.objects.all(), write_only=True)
    transportation = serializers.PrimaryKeyRelatedField(
        queryset=Transportation.objects.all(), write_only=True)

    class Meta:
        model = Order
        fields = ('uuid', 'creditcard', 'transportation')

class HistorySerializer(serializers.ModelSerializer):
    products = OrderInfoDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ('id', 'final_price', 'products', 'updated_at')

class TransportationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transportation
        fields = ('id', 'name', 'description', 'price')
