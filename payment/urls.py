from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', 
        CreditCardAction.as_view(),
        name="payment-creator"),
    url(r'^delete/(?P<token>\w+)/(?P<credit_id>[0-9]+)$', 
        CreditCardDeleteAction.as_view(),
        name="payment-delete"),
]
