from payment.models import BankAccount
from payment.serializers import BankAccountSerializer

from rest_framework import generics

# Create your views here.
class BankAccountAction(generics.ListCreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
