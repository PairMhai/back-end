from django.conf.urls import url
from membership import views

urlpatterns = [
    url(r'^$', views.create),
]
