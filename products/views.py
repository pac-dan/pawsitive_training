from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, ProductCategory
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProductStockUpdateForm, ProductForm
from basket.models import Basket

@staff_member_required
def update_stock(request, product_id):
    """
    A view to update the stock level of a product.
    """
    product = get_object_or_404(Product, id=product_id)

    # Check if the form has been submitted.
    if request.method == 'POST':
        form = ProductStockUpdateForm(request.POST, instance=product)

        # If the form is valid, save the product and display a success message.
        if form.is_valid():
            form.save()
            messages.success(request, "Stock updated successfully!")
            return redirect('products:stock_list')
        
        # If the form is invalid, display an error message.
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductStockUpdateForm(instance=product)
    return render(request, 'products/update_stock.html', {'form': form, 'product': product})

@staff_member_required
def stock_list(request):
    """
    A view to display a list of products and their stock levels.
    """
    products = Product.objects.all()
    return render(request, 'products/stock_list.html', {'products': products})

def category_products(request, category_slug):
    """
    Displays a paginated list of products for a given category.
    """

    # Get the category object based on the slug.
    category = get_object_or_404(ProductCategory, slug=category_slug)
    products = category.products.all() 
    paginator = Paginator(products, 8)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get basket information for each product
    basket = Basket(request)
    products_with_basket_info = []
    
    for product in page_obj:
        product_id_str = str(product.id)
        current_quantity = basket.basket.get(product_id_str, {}).get('quantity', 0)
        can_add_more = current_quantity < product.stock
        
        products_with_basket_info.append({
            'product': product,
            'current_basket_quantity': current_quantity,
            'can_add_more': can_add_more,
            'available_to_add': product.stock - current_quantity
        })
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'products_with_basket_info': products_with_basket_info,
    }
    return render(request, 'products/products_category.html', context)

def products_display(request):
    """
    Displays a paginated list of all products.
    """

    # Get all products and paginate them.
    products = Product.objects.all()
    paginator = Paginator(products, 8)  # 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get basket information for each product
    basket = Basket(request)
    products_with_basket_info = []
    
    for product in page_obj:
        product_id_str = str(product.id)
        current_quantity = basket.basket.get(product_id_str, {}).get('quantity', 0)
        can_add_more = current_quantity < product.stock
        
        products_with_basket_info.append({
            'product': product,
            'current_basket_quantity': current_quantity,
            'can_add_more': can_add_more,
            'available_to_add': product.stock - current_quantity
        })
    
    context = {
        'page_obj': page_obj,
        'products_with_basket_info': products_with_basket_info,
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
    
    # Get basket information for each product
    basket = Basket(request)
    products_with_basket_info = []
    
    for product in page_obj:
        product_id_str = str(product.id)
        current_quantity = basket.basket.get(product_id_str, {}).get('quantity', 0)
        can_add_more = current_quantity < product.stock
        
        products_with_basket_info.append({
            'product': product,
            'current_basket_quantity': current_quantity,
            'can_add_more': can_add_more,
            'available_to_add': product.stock - current_quantity
        })
    
    context = {
        'page_obj': page_obj,
        'search_term': query,
        'products_with_basket_info': products_with_basket_info,
    }
    return render(request, 'products/products_category.html', context)


def product_detail(request, pk):
    """
    Displays the detail view of a single product.
    """
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/products_detail.html', {'product': product})


@staff_member_required
def create_product(request):
    """
    View for staff to create a new product.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('products:product_detail', pk=product.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
    
    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Create New Product',
        'button_text': 'Create Product'
    })


@staff_member_required
def edit_product(request, product_id):
    """
    View for staff to edit an existing product.
    """
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('products:product_detail', pk=product.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/product_form.html', {
        'form': form,
        'product': product,
        'title': f'Edit {product.name}',
        'button_text': 'Update Product'
    })


@staff_member_required
def delete_product(request, product_id):
    """
    View for staff to delete a product.
    """
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" has been deleted.')
        return redirect('products:stock_list')
    
    return render(request, 'products/product_confirm_delete.html', {
        'product': product
    })