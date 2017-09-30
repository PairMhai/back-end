from django.conf.urls import url
from comment.views import *

urlpatterns = [
    url(r'^$', CommentCreator.as_view(), name="comment-creator"),
    url(r'^all$', CommentList.as_view(), name="comment-list"),
]
