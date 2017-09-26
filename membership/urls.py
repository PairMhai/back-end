from django.conf.urls import url, include
from membership.views import CustomerAction, CustomerDetail, ClassDetail

urlpatterns = [
    url(r'^', include('rest_auth.urls')),
    url(r'^register/', include('rest_auth.registration.urls')),
    # url(r'^$', CustomerAction.as_view(), name="membership"),
    # url(r'^(?P<pk>[0-9]+)$', CustomerDetail.as_view(), name="membership-detail"),
    # url(r'^class/(?P<pk>[0-9]+)$', ClassDetail.as_view(), name="membership-class"),
]
