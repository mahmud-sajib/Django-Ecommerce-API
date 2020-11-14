from rest_framework import serializers

from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        # Model to be serialized
        model = Category
        # Fields to be serialized 
        fields = ('name', 'description') 