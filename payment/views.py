from payment.models import CreditCard
from payment.serializers import FullCreditCardSerializer

from rest_framework import generics
from rest_framework.exceptions import NotAcceptable
from utilities.classes.database import ImpDestroyByTokenView
from utilities.methods.database import get_customer_by_uid

# Create your views here.
class CreditCardAction(generics.CreateAPIView):
    queryset = CreditCard.objects.all()
    serializer_class = FullCreditCardSerializer

class CreditCardDeleteAction(ImpDestroyByTokenView):
    queryset = CreditCard.objects.all()
    serializer_class = FullCreditCardSerializer
    credit_id = "credit_card_id"

    def update_kwargs(self, **kwargs):
        self.kwargs[self.credit_id] = kwargs.get('credit_id')
        return super(CreditCardDeleteAction, self).update_kwargs(**kwargs)
    
    def get_object(self):
        obj = super(CreditCardDeleteAction, self).get_object()
        cust = get_customer_by_uid(obj.id)
        try: 
            return CreditCard.objects.get(
                id=self.kwargs[self.credit_id],
                customer=cust
            )
        except:
            raise NotAcceptable(detail="your customer and creditcard not matches.")
