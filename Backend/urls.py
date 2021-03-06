"""Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from version.views import Index as V_Index
from landingpage.views import Index as L_Index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^membership/', include('membership.urls')),
    url(r'^payment/', include('payment.urls')),
    url(r'^catalog/', include('catalog.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^comment/', include('comment.urls')),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^version$', V_Index.as_view(), name='version'),
    url(r'^$', L_Index.as_view(), name='landing-page'),
]
