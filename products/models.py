from django.db import models

class Product(models.Model):
    sku = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/')  
    brand = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.name or 'Unnamed Product'
 
