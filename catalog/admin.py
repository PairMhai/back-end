from django.contrib import admin
from .models import Design, Material, Product, Promotion, Image

class DesignAdmin(admin.ModelAdmin):
    class Meta:
        model = Design
    def save_model(self, request, obj, form, change):
        obj.save()
        Product.objects.create(material=None, design=Design.objects.get(pk=obj.id)).save()

class MaterialAdmin(admin.ModelAdmin):
    class Meta:
        model = Material
    def save_model(self, request, obj, form, change):
        obj.save()
        Product.objects.create(material=Material.objects.get(pk=obj.id), design=None).save()

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('design', 'material')
    class Meta:
        model = Product
    def has_add_permission(self, request):
        return False

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
