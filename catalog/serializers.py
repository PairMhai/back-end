from catalog.models import Material, Design, Image, Product, Promotion
from rest_framework import serializers

from collections import OrderedDict
from utilities.classes.database import ThaiDateTimeField


class PromotionSerializer(serializers.ModelSerializer):
    start = ThaiDateTimeField(source='start_date')
    end = ThaiDateTimeField(source='end_date')

    class Meta:
        model = Promotion
        fields = ('name', 'description', 'discount', 'image_name',
                  'status', 'start', 'end')  # , 'id'


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('id', 'file_name')


class FullImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('id', 'file_name', 'design')


class MiniMaterialSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='get_product_id')

    class Meta:
        model = Material
        fields = ('product_id', 'id', 'name',
                  'description', 'color',
                  'image_name')

        
class MiniDesignSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='get_product_id')
    images = ImageSerializer(many=True)
    material = MiniMaterialSerializer()

    class Meta:
        model = Design
        fields = ('product_id', 'id', 'name', 'description', 'material',
                  'images')

        
class ListMaterialSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='get_product_id')
    discounted_price = serializers.CharField(source='get_discount_price')

    class Meta:
        model = Material
        fields = ('product_id', 'id', 'name',
                  'description', 'price', 'discounted_price',
                  'color', 'image_name')


class MaterialSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='get_product_id')
    discounted_price = serializers.CharField(source='get_discount_price')

    associate_promotions = PromotionSerializer(
        source='get_associate_promotion', many=True)

    class Meta:
        model = Material
        fields = ('product_id', 'id', 'name',
                  'quantity', 'description',
                  'price', 'discounted_price',
                  'color', 'image_name',
                  'associate_promotions')


class DesignSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(source='get_price')
    discounted_price = serializers.CharField(source='get_discount_price')

    product_id = serializers.IntegerField(source='get_product_id')
    images = ImageSerializer(many=True)
    material = MiniMaterialSerializer()
    associate_promotions = PromotionSerializer(
        source='get_associate_promotion', many=True)

    class Meta:
        model = Design
        fields = ('product_id', 'id',
                  'name', 'description',
                  'price', 'discounted_price',
                  'material', 'images',
                  'associate_promotions')

    def validate_product_id(self, value):
        print(value)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'design', 'material')


class ProductDetailSerializer(serializers.ModelSerializer):
    design = MiniDesignSerializer(required=False)
    material = MiniMaterialSerializer(required=False)

    class Meta:
        model = Product
        fields = ('id', 'design', 'material')

    def to_representation(self, instance):
        result = super(ProductDetailSerializer,
                       self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])
