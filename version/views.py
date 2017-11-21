from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from django.contrib.admin.models import LogEntry

class Index(APIView):

    def get(self, request, format=None):
        env = request._request.environ
        obj = "{}".format(env.get("HOME"))
        msg = "{} {}".format(env.get("REQUEST_METHOD"), env.get("PATH_INFO"))

        LogEntry.objects.log_action(
            1, None, settings.VERSION, obj, 1, msg
        )
        return Response({'version': settings.VERSION})
