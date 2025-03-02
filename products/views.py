from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product

def products_display(request):
    """
    Displays a paginated list of all products.
    """
    products = Product.objects.all()
    paginator = Paginator(products, 8)  # 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'products/products_display.html', context)

def search(request):
    """
    Searches for products based on a query string provided via GET parameters.
    """
    query = None
    products = Product.objects.all()
    
    # Check if a search query exists and is non-empty.
    if 'q' in request.GET and request.GET['q']:
        query = request.GET['q']
        # Construct Q objects to search both name and description.
        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)
    elif 'q' in request.GET:
        messages.error(request, "You didn't enter any search criteria!")
        return redirect(reverse('products:products_display'))
    
    # Paginate the filtered products (8 per page).
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_term': query,
    }
    return render(request, '../templates/products/products_display.html', context)


def product_detail(request, pk):
    """
    Displays the detail view of a single product.
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, '../templates/products/products_detail.html', {'product': product})