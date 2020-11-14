from django.db import models
from api.user.models import CustomUser
from api.product.models import Product

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_names = models.CharField(max_length=150)
    total_products = models.CharField(max_length=250, default=0)
    total_amount = models.CharField(max_length=250, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=150, default=0)
    
    def __str__(self):
        return f"{self.product_name}"




