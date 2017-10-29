from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings

class Index(APIView):
    def get(self, request, format=None):
        return Response({'version': settings.VERSION})
