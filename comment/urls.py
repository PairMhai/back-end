from django.conf.urls import url
from comment.views import *

urlpatterns = [
    url(r'^$', CommentListAndCreateView.as_view(), name="comment")
]
