from django.conf.urls import url, include
from membership.views import CustomerDetail, UserDetail, ClassDetail, ConfirmEmailView, completed_register  # , CustomerList

urlpatterns = [
    # url(r'^django-auth', include('django.contrib.auth.urls')),
    url(r'^', include('rest_auth.urls')),
    url(r'^register/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email1'),
    url(r'^register/', include('rest_auth.registration.urls')),
    url(r'^register/completed', completed_register, name='account_email_verification_sent'),
    url(r'^cust/(?P<token>\w+)$', CustomerDetail.as_view(), name="membership-cust-detail"),
    url(r'^user/(?P<token>\w+)$', UserDetail.as_view(), name="membership-user-detail"),
    # WAITING: update it's to return class by `customer id` instead of `class id`
    url(r'^class/(?P<pk>[0-9]+)$', ClassDetail.as_view(), name="membership-class-detail"),
]
