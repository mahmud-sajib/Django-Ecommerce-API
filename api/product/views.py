from rest_framework import viewsets
from .serializers import ProductSerializer
from .models import Product

# Create your views here.

# Product View
class ProductViewSet(viewsets.ModelViewSet):
    # Operations to be performed
    queryset = Product.objects.all().order_by('id')
    # Class responsible for serializing the data 
    serializer_class = ProductSerializer 
