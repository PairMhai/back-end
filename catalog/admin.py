from django.contrib import admin
from .models import Design, Material, Product, Promotion, Image

class DesignAdmin(admin.ModelAdmin):
    class Meta:
        model = Design

class MaterialAdmin(admin.ModelAdmin):
    class Meta:
        model = Material

class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product

class PromotionAdmin(admin.ModelAdmin):
    class Meta:
        model = Promotion

class ImageAdmin(admin.ModelAdmin):
    class Meta:
        model = Image

admin.site.register(Design, DesignAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(Image, ImageAdmin)
