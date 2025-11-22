from django import forms
from .models import Product, ProductCategory

class ProductStockUpdateForm(forms.ModelForm):
    """
    Form for staff to update product stock levels.
    """
    class Meta:
        model = Product
        fields = ['stock']
        widgets = {
            'stock': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0,
                'placeholder': 'Enter stock quantity'
            }),
        }
        labels = {
            'stock': 'Stock Quantity',
        }


class ProductForm(forms.ModelForm):
    """
    Form for staff to create and edit products.
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock', 'sku', 'brand', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter product description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter SKU (optional)'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter brand name (optional)'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'name': 'Product Name',
            'description': 'Description',
            'price': 'Price ($)',
            'category': 'Category',
            'stock': 'Stock Quantity',
            'sku': 'SKU',
            'brand': 'Brand',
            'image': 'Product Image',
        }
        help_texts = {
            'stock': 'Number of items available in stock',
            'price': 'Product price in USD',
            'sku': 'Stock Keeping Unit (optional)',
        }
    
    def clean_price(self):
        """Ensure price is positive."""
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise forms.ValidationError('Price cannot be negative.')
        return price
    
    def clean_stock(self):
        """Ensure stock is not negative."""
        stock = self.cleaned_data.get('stock')
        if stock and stock < 0:
            raise forms.ValidationError('Stock cannot be negative.')
        return stock