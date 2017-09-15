from catalog.models import Material, Design, Pattern
from catalog.serializers import MaterialSerializer, DesignSerializer, PatternSerializer
# from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics

#Create your views here.
class MaterialList(generics.ListAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class MaterialDetail(generics.RetrieveAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class DesignList(generics.ListAPIView):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer

class DesignDetail(generics.RetrieveAPIView):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer

class PatternList(generics.ListAPIView):
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializer

class PatternDetail(generics.RetrieveAPIView):
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializer
