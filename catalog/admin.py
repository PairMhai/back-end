from django.contrib import admin
from .models import Design, Material, Pattern

class DesignAdmin(admin.ModelAdmin):
    class Meta:
        model = Design

class MaterialAdmin(admin.ModelAdmin):
    class Meta:
        model = Material

class PatternAdmin(admin.ModelAdmin):
    class Meta:
        model = Pattern

admin.site.register(Design, DesignAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Pattern, PatternAdmin)
