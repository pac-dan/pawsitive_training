from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Product

def products_display(request):
    products = Product.objects.all().order_by('name')
    paginator = Paginator(products, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, '../templates/products/products_display.html', {'page_obj': page_obj})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, '../templates/products/products_detail.html', {'product': product})