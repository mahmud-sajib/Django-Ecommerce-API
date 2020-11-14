from django.db import models
from api.category.models import Category

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.CharField(max_length=50)
    stock = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"



