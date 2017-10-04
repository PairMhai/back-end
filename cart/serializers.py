from rest_framework import serializers

from rest_framework.authtoken.models import Token
from cart.models import Order, OrderInfo, Transportation
from catalog.models import Product
from membership.models import Customer
from payment.models import CreditCard

from membership.serializers import FullCustomerSerializer
from catalog.serializers import ProductSerializer


class OrderInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    pid = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = OrderInfo
        fields = ('product', 'pid', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(max_length=200)
    creditcard = serializers.PrimaryKeyRelatedField(
        queryset=CreditCard.objects.all(), write_only=True)
    transportation = serializers.PrimaryKeyRelatedField(
        queryset=Transportation.objects.all(), write_only=True)
    products = OrderInfoSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'creditcard',
                  'transportation', 'products')

    def validate_customer(self, value):
        try:
            return Customer.objects.get(id=Token.objects.get(key=value).user_id)
        except Token.DoesNotExist:
            raise serializers.ValidationError(
                "customer key accept either id or token.")

    def create(self, validated_data):
        orders_info = validated_data.pop('products')
        validated_data.update({'total_price': 0})
        validated_data.update({'total_product': len(orders_info)})
        order = Order.objects.create(**validated_data)
        # print("order id {}".format(order))
        # FIXME: incase order same pid (should merge to 1 row)
        for info in orders_info:
            info.update({'order': order})
            order_info = OrderInfo.objects.create(**info)
            order.total_price += order_info.product.get_price()
        # print("summary product price:", order.total_price)
        # print("transportation price:", order.transportation.price)
        order.total_price += order.transportation.price
        # print("total price:", order.total_price)
        discount = order.total_price * (order.customer.classes.discount / 100)
        # print("discount:", discount)
        order.total_price -= discount
        # print("final price:", order.total_price)
        order.save()
        return order

class TransportationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transportation
        fields = ('id', 'name', 'description', 'price')
