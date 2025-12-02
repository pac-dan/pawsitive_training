from django.db import models
from django.utils.text import slugify


class ProductCategory(models.Model):
    """
    Model to store product categories for organizing products.
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Create a slug when saving the product category.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Product Categories"


class Product(models.Model):
    """
    Model to store product details.
    """
    sku = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    brand = models.CharField(max_length=255, blank=True, null=True)

    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
        blank=True
    )

    stock = models.IntegerField(default=0, help_text="Available stock for this product")

    def __str__(self):
        """
        Return a string representation of the product.
        """
        return self.name or 'Unnamed Product'
