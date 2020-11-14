from rest_framework import serializers

from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        # Model to be serialized
        model = Order
        # Fields to be serialized 
        fields = ('user',) 