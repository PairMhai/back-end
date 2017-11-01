from membership.models import Customer
from catalog.models import Product, Design
from cart.models import Order, OrderInfo, Transportation
from cart.serializers import TransportationSerializer, OrderSerializer, OrderCreateSerializer, HistorySerializer, CalculateOrderSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from django.forms.models import model_to_dict

from utilities.methods.database import get_customer_by_uid
from utilities.classes.database import ImpListByTokenView


class TransportationListView(generics.ListAPIView):
    queryset = Transportation.objects.all()
    serializer_class = TransportationSerializer


class OrderCreatorView(generics.CreateAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        from django.core.cache import cache

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uuid = serializer.validated_data.get('uuid')
        creditcard = serializer.validated_data.get('creditcard')
        transportation = serializer.validated_data.get('transportation')
        ttl = cache.ttl("order-{}".format(uuid))
        # print(ttl)
        if (ttl == 0):
            return Response({"detail": "you order is timeout, try again."}, status=status.HTTP_400_BAD_REQUEST)

        order_calculation = cache.get("order-{}".format(uuid))
        # print(order_calculation)
        products = []
        for pid, quantity in order_calculation.get('products_id').items():
            products.append({
                "pid": pid,
                "quantity": quantity
            })
        # print(products)
        for d in products:
            p = Product.objects.get(id=d.get("pid"))
            q = d.get("quantity")
            prd = p.get_object
            if isinstance(prd, Design):
                total_quantity = prd.yard * q
                quantity = prd.material.quantity
                prd.material.quantity = quantity - total_quantity
                prd.save()
            else:
                prd.quantity = prd.quantity - q
                prd.save()
        data = {
            "customer": order_calculation.get('customer_id'),
            "products": products,
            "final_price": order_calculation.get('total_price') + transportation.price,
            'creditcard': creditcard.id,
            "transportation": transportation.id
        }

        order_serializer = OrderCreateSerializer(data=data)
        order_serializer.is_valid(raise_exception=True)
        # create order
        self.perform_create(order_serializer)

        headers = self.get_success_headers(order_serializer.data)
        # order = Order.objects.get(pk=order_serializer.data.get('id'))
        tran_serializer = TransportationSerializer(
            data=model_to_dict(transportation))
        tran_serializer.is_valid(raise_exception=True)

        return Response({
            'final_price': order_calculation.get('total_price') + transportation.price,
            'total_product': len(products),
            'transportation': tran_serializer.validated_data
        }, status=status.HTTP_201_CREATED, headers=headers)


class OrderCalculateView(APIView):

    def post(self, request, format=None):
        from django.core.cache import cache
        import uuid

        serializers = CalculateOrderSerializer(data=request.data)
        if (serializers.is_valid()):
            full_price = 0
            customer_discount = 0
            total_price = 0
            product_event_price = 0

            data = serializers.validated_data
            customer = data.get('customer')
            products = data.get('products')
            # dict={1:2, 4,1} PRODUCT_ID:QUANTITY
            products_id = dict()
            error_products = []

            for d in products:
                p = d.get('product')
                q = d.get('quantity')
                a = p.get_object()
                if isinstance(a, Design):
                    total_yard = a.yard * q
                    mat = a.material
                    if total_yard > mat.quantity:
                        error_products.append(p)
                else:
                    if q > a.quantity:
                        error_products.append(p)

                if (p.id in products_id):
                    products_id[p.id] += q
                else:
                    products_id[p.id] = q
                # get_discount_price
                full_price += (p.get_price() * q)
                product_event_price += p.get_discount_price()  # should be discounted price
            # calculate from full price
            customer_discount = full_price * (customer.classes.discount / 100)
            total_price = product_event_price - customer_discount
            if (total_price < 0):
                total_price = 0
            # "event_price": product_event_price, # can calculate by `event_discount`

            if error_products.count() > 0:
                detail = str(error_products) + " doesn't have enough stocks."
                return Response({"detail": detail}, status=status.HTTP_400_BAD_REQUEST)

            data = {
                "calculate_id": uuid.uuid4(),
                "customer_id": customer.id,
                "products_id": products_id,
                "full_price": full_price,
                "customer_discount": customer_discount,
                "event_discount": full_price - product_event_price,
                "total_price": total_price
            }

            # Example data
            # {
            #       'calculate_id': UUID('4bf1b714-4938-47c6-b85f-3aff18c86e54'),
            #       'customer_id': 2,
            #       'products_id':
            #               {
            #                   1: 3,
            #                   2: 4
            #               },
            #       'full_price': Decimal('36000.0000'),
            #       'customer_discount': Decimal('5400.0000000'),
            #       'event_discount': Decimal('34271.00000000'),
            #       'total_price': 0
            # }

            # save calculation price
            cache.set("order-{}".format(data.get('calculate_id')),
                      data, timeout=60 * 10)  # second 60 * 10
            # remove unneccessary key
            data.pop('customer_id', None)
            data.pop('products_id', None)

            return Response(data)
        else:
            return Response({"detail": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)


class HistoryView(ImpListByTokenView):
    queryset = Order.objects.all()
    serializer_class = HistorySerializer
    id_str = 'customer_id'

    def set_id(self, token):
        self.uid = get_customer_by_uid(token.user_id).id

    def get_queryset(self):
        return super(HistoryView, self).get_queryset().filter(customer_id=self.uid)
