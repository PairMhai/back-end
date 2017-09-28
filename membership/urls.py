from django.conf.urls import url, include
from membership.views import CustomerDetail, UserDetail, ClassDetail # , CustomerAction

urlpatterns = [
    url(r'^django-auth/', include('django.contrib.auth.urls')),
    url(r'^', include('rest_auth.urls')),
    url(r'^register/', include('rest_auth.registration.urls')),
    # url(r'^$', CustomerAction.as_view(), name="membership"),
    url(r'^cust/(?P<pk>[0-9]+)$', CustomerDetail.as_view(), name="membership-cust-detail"),
    url(r'^user/(?P<pk>[0-9]+)$', UserDetail.as_view(), name="membership-user-detail"),
    # FIXME: update it's to return class by `customer id` instead of `class id`
    url(r'^class/(?P<pk>[0-9]+)$', ClassDetail.as_view(), name="membership-class"),
]
