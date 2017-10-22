from catalog.models import Material, Design, Image, Product, Promotion
from rest_framework import serializers



class MaterialSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='get_product_id')
    discount_price = serializers.CharField(source='get_discount_price')

    class Meta:
        model = Material
        fields = ('product_id', 'id', 'name', 'quantity', 'description', 'quantity', 'price', 'discount_price', 'color', 'image_name')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'file_name')

class FullImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'file_name', 'design')

class DesignSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='get_product_id')
    images = ImageSerializer(many=True)
    material_name = serializers.CharField(source='get_material_name')
    material_color = serializers.CharField(source='get_color')
    discount_price = serializers.CharField(source='get_discount_price')

    class Meta:
        model = Design
        fields = ('product_id', 'id', 'name', 'description', 'price', 'discount_price', 'images', 'material_name', 'material_color')
    def validate_product_id(self, value):
        print(value)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'design', 'material')

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ('name', 'image_name') # , 'id'
