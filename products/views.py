from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, ProductCategory
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProductStockUpdateForm

@staff_member_required
def update_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductStockUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock updated successfully!")
            return redirect('products:stock_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductStockUpdateForm(instance=product)
    return render(request, 'products/update_stock.html', {'form': form, 'product': product})

@staff_member_required
def stock_list(request):
    products = Product.objects.all()
    return render(request, 'products/stock_list.html', {'products': products})

def category_products(request, category_slug):
    """
    Displays a paginated list of products for a given category.
    """
    category = get_object_or_404(ProductCategory, slug=category_slug)
    products = category.products.all() 
    paginator = Paginator(products, 8)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, '../templates/products/products_category.html', context)

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
    return render(request, '../templates/products/products_category.html', context)


def product_detail(request, pk):
    """
    Displays the detail view of a single product.
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, '../templates/products/products_detail.html', {'product': product})