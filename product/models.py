from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
PRODUCT_TYPES = [
    ('Wallpaper', 'Wallpaper'),
    ('Artifact', 'Artifact'),
]

class Product(models.Model):
    title = models.CharField(max_length=200, null=False)
    type = models.CharField(max_length=9, choices=PRODUCT_TYPES, null=False)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, auto_created=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:list_product')
