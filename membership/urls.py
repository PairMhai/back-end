from django.conf.urls import url
from membership.views import CustomerAction
from membership.views import CustomerDetail

urlpatterns = [
    url(r'^$', CustomerAction.as_view()),
    url(r'^id/(?P<pk>[0-9]+)$', CustomerDetail.as_view()),
]
