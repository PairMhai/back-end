from django.conf.urls import url
from membership.views import CustomerAction, CustomerDetail, ClassDetail

urlpatterns = [
    url(r'^$', CustomerAction.as_view()),
    url(r'^id/(?P<pk>[0-9]+)$', CustomerDetail.as_view()),
    url(r'^class/(?P<pk>[0-9]+)$', ClassDetail.as_view()),
]
