from django.contrib import admin
from product.models import Product


# Register your models here.

@admin.register(Product)
class ProductFormModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'image', 'description', 'created_at', 'updated_at', 'user']
