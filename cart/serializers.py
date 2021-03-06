from rest_framework import serializers

from rest_framework.authtoken.models import Token
from cart.models import Order, OrderInfo, Transportation
from catalog.models import Product
from membership.models import Customer
from payment.models import CreditCard

from membership.serializers import FullCustomerSerializer
from catalog.serializers import ProductSerializer, ProductDetailSerializer

class TransportationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transportation
        fields = ('id', 'name', 'description', 'price')

class TransportationIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transportation
        fields = ('id')

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
    transportation = serializers.IntegerField()

    def validate_customer(self, value):
        try:
            return Customer.objects.get(user_id=Token.objects.get(key=value).user_id)
        except Token.DoesNotExist:
            raise serializers.ValidationError(
                "customer key accept either id or token.")
        except Customer.DoesNotExist:
            raise serializers.ValidationError(
                "you are no our customer.")

    def validate_transportation(self, value):
        try:
            return Transportation.objects.get(pk=value)
        except Transportation.DoesNotExist:
            raise serializers.ValidationError(
                "transportation id invalid.")


class OrderCreateSerializer(serializers.ModelSerializer):
    products = OrderInfoSerializer(many=True)

    class Meta:
        model = Order
        fields = ('products', 'total_product', 'final_price',
                  'customer', 'creditcard', 'transportation', 'address')

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
    # transportation = serializers.PrimaryKeyRelatedField(
        # queryset=Transportation.objects.all(), write_only=True)

    class Meta:
        model = Order
        fields = ('uuid', 'creditcard', 'address')



class HistorySerializer(serializers.ModelSerializer):
    products = OrderInfoDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'final_price', 'products', 'created_at', 'updated_at')
