from payment.models import CreditCard
from payment.serializers import FullCreditCardSerializer

from rest_framework import generics

# Create your views here.
class CreditCardAction(generics.CreateAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = FullCreditCardSerializer
