from catalog.models import Material, Design, Promotion
from catalog.serializers import MaterialSerializer, DesignSerializer, PromotionSerializer

from rest_framework import generics


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


class PromotionList(generics.ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

    def filter_queryset(self, queryset):
        # might slow query down
        for q in queryset:
            s = q.update_status()
        new_q = queryset.filter(status=True)
        return new_q


# class PromotionDetail(generics.RetrieveAPIView):
#     queryset = Promotion.objects.all()
#     serializer_class = PromotionSerializer
