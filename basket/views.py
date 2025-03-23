from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from products.models import Product
from .models import Basket  

@require_POST
def basket_add(request, product_id):
    """
    A view to add a product to the shopping basket.
    """

    # Get the product and add it to the basket
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    basket.add(product=product, quantity=1, update_quantity=False)

    # Get the updated quantity and price
    product_id_str = str(product.id)
    new_quantity = basket.basket[product_id_str]['quantity']
    product_price = product.price
    line_total = product_price * new_quantity
    
    # Prepare the data to return as JSON
    data = {
        'grand_total': str(basket.get_total_price()),
        'basket_items': len(basket),
        'product_id': product.id, 
        'product_quantity': new_quantity,
        'product_price': str(product_price),  # Unit price
        'line_total': str(line_total),          # Updated subtotal for that product
        'message': 'Product added to basket successfully!'
    }

    return JsonResponse(data)

@require_POST
def basket_remove(request, product_id):
    """
    A view to remove a product from the shopping basket.
    """

    # Get the product and remove it from the basket
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Remove one unit of the product (or the entire product if quantity == 1)
    basket.remove(product)
    
    # Get the updated quantity and price
    product_id_str = str(product.id)
    new_quantity = basket.basket.get(product_id_str, {}).get('quantity', 0)
    product_price = product.price
    line_total = product_price * new_quantity
    
    # Prepare the data to return as JSON
    data = {
        'grand_total': str(basket.get_total_price()),
        'basket_items': len(basket),
        'product_id': product.id,
        'product_quantity': new_quantity,
        'product_price': str(product_price),
        'line_total': str(line_total),
    }

    return JsonResponse(data)

def basket_detail(request):
    """
    A view to render the shopping basket page.
    """

    # Get the basket items
    basket = Basket(request)
    basket_items = []

    # Iterate over key-value pairs where key is product_id
    for product_id, item in basket.basket.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = item['quantity']
        total = product.price * quantity
        price = product.price
        basket_items.append({
            'product': product,
            'quantity': quantity,
            'total': total,
            'price': price,
        })

    # Prepare the context
    context = {
        'basket': basket_items,
        'total': basket.get_total_price(),
    }

    return render(request, 'basket_detail.html', context)

