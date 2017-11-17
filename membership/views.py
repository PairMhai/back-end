from membership.models import User, Customer, Class
from allauth.account.models import EmailConfirmationHMAC

from membership.serializers import FullCustomerSerializer, CustomerSerializer, FullUserSerializer, HalfUserSerializer, ClassSerializer

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from utilities.classes.database import ImpDetailByTokenView
from utilities.classes.database import ImpUpdateByTokenView


class CustomerDetail(ImpDetailByTokenView):
    queryset = Customer.objects.all()
    serializer_class = FullCustomerSerializer
    user_id = 'user_id'


class UserDetail(ImpDetailByTokenView, ImpUpdateByTokenView):
    queryset = User.objects.all()
    serializer_class = FullUserSerializer


class ClassDetail(generics.RetrieveAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class ConfirmEmailView(APIView):

    def get(self, request, key, format=None):
        confirmation = EmailConfirmationHMAC.from_key(key)
        if not confirmation:
            return Response({"detail": "wrong confirm key or expired"}, status=status.HTTP_400_BAD_REQUEST)
        email = confirmation.confirm(self.request)
        if email is None:
            return Response({"detail": "this email already confirmed."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"email": email.email})

# never used, BUT needed


def completed_register(request):
    return Response()
