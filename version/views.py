from django.http import JsonResponse
from django.views import View

from django.conf import settings

class Index(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'version': settings.VERSION})
