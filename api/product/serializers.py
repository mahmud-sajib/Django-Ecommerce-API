from rest_framework import serializers

from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    # Get the image url by serializing `ImageField`
    image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=True, required=False)

    class Meta:
        # Model to be serialized
        model = Product
        # Fields to be serialized 
        fields = ('id', 'name', 'description', 'price', 'stock', 'image', 'category') 