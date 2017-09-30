from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', CreditCardAction.as_view(), name="payment"),
]
