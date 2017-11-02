from rest_framework import generics

from catalog.models import Material, Design, Promotion
from catalog.serializers import ListMaterialSerializer, MaterialSerializer, DesignSerializer, PromotionSerializer

from utilities.methods.database import update_all_status_promotions


class MaterialList(generics.ListAPIView):
    queryset = Material.objects.all()
    serializer_class = ListMaterialSerializer


class MaterialDetail(generics.RetrieveAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class DesignList(generics.ListAPIView):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer


class DesignDetail(generics.RetrieveAPIView):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer


class PromotionList(generics.ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

    def filter_queryset(self, queryset):
        return update_all_status_promotions(queryset)


# class PromotionDetail(generics.RetrieveAPIView):
#     queryset = Promotion.objects.all()
#     serializer_class = PromotionSerializer
