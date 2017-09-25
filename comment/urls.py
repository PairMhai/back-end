from django.conf.urls import url
from comment.views import *

urlpatterns = [
    url(r'^$', CommentCreator.as_view()),
]
