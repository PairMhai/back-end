from django.shortcuts import render
from comment.models import Comment
from comment.serializers import CommentSerializer

from rest_framework import generics

#Create your views here.
class CommentListAndCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
