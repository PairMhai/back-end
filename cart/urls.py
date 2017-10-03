from django.conf.urls import url
from cart.views import *

urlpatterns = [
    url(r'^transportation/$', TransportationListView.as_view(), name="transportation-list"),
]
