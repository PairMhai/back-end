from django.contrib import admin
from .models import Order, OrderInfo, Transportation

class OrderInfoInline(admin.TabularInline):
    model = OrderInfo
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderInfoInline]
    class Meta:
        model = Order

class OrderInfoAdmin(admin.ModelAdmin):
    class Meta:
        model = OrderInfo

class TransportationAdmin(admin.ModelAdmin):
    class Meta:
        model = Transportation

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)
admin.site.register(Transportation, TransportationAdmin)
