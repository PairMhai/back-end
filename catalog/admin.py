from django.contrib import admin
from django import forms
from django.utils import timezone
from utilities.methods.other import is_between_date
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

class PromotionForm(forms.ModelForm):

    class Meta:
        model = Promotion
        fields = ('name', 'image_name', 'discount', 'status', 'start_date',
                'end_date', 'description', 'products')

    def __init__(self, *args, **kwargs):
        super(PromotionForm, self).__init__(*args, **kwargs)
        if self.instance.start_date is not None and self.instance.end_date is not None:
            self.fields['status'].disabled = True

class PromotionAdmin(admin.ModelAdmin):
    form = PromotionForm

class ImageAdmin(admin.ModelAdmin):
    class Meta:
        model = Image

admin.site.register(Design, DesignAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(Image, ImageAdmin)
