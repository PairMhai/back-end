from django.conf.urls import url
from catalog.views import *

urlpatterns = [
    url(r'^materials$', MaterialList.as_view()),
    url(r'^material/(?P<pk>[0-9]+)$', MaterialDetail.as_view()),
    url(r'^designs$', DesignList.as_view()),
    url(r'^design/(?P<pk>[0-9]+)$', DesignDetail.as_view()),
    # url(r'^products$', DesignDetail.as_view()),
    # url(r'^patterns$', PatternList.as_view()),
    # url(r'^pattern/(?P<pk>[0-9]+)$', PatternDetail.as_view()),
]
