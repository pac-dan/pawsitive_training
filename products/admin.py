from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductCategory

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'stock', 'image_preview')
    readonly_fields = ('image_preview',)
    list_filter = ('category', 'brand')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="auto" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
