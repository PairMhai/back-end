from catalog.models import Material, Design, Pattern
from rest_framework import serializers

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'name',
                  'quantity', 'price')

class DesignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Design
        fields = ('id', 'name', 'price')

class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = ('id', 'name',
                  'primary_color', 'description')
