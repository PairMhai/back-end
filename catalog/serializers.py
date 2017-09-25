from catalog.models import Material, Design, Pattern, Image
from rest_framework import serializers

class SoftMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'name', 'price')

class HardMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'name',
                  'quantity', 'price')

class DesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Design
        fields = ('id', 'name', 'price')

class SoftPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = ('id', 'name')

class HardPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = ('id', 'name',
                  'primary_color', 'description')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'material_id')
