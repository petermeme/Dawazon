from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models

from vendor.models import Vendor

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default="", max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']
    
    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    is_sale = models.BooleanField(default=True)
    on_discount = models.BooleanField(default = False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    image = models.ImageField(upload_to='uploads/products', null=True, default=False )

    class Meta:
        ordering = ['-date_added']
    
    def __str__(self):
        return self.title
