from django.contrib import admin
from .models import Design, Material, Product, Promotion

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

admin.site.register(Design, DesignAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Promotion, PromotionAdmin)