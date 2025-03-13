from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from products.models import Product
from .models import Basket  

@require_POST
def basket_add(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    basket.add(product=product, quantity=1, update_quantity=False)

    product_id_str = str(product.id)
    new_quantity = basket.basket[product_id_str]['quantity']
    product_price = product.price
    line_total = product_price * new_quantity
    
    data = {
        'grand_total': str(basket.get_total_price()),
        'basket_items': len(basket),
        'product_id': product.id, 
        'product_quantity': new_quantity,
        'product_price': str(product_price),  # Unit price
        'line_total': str(line_total),          # Updated subtotal for that product
    }
    return JsonResponse(data)

@require_POST
def basket_remove(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Remove one unit of the product (or the entire product if quantity == 1)
    basket.remove(product)
    
    product_id_str = str(product.id)
    new_quantity = basket.basket.get(product_id_str, {}).get('quantity', 0)
    product_price = product.price
    line_total = product_price * new_quantity
    
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
    basket = Basket(request)
    basket_items = []
    for product_id, item in basket.basket.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = item['quantity']
        total = product.price * quantity
        basket_items.append({
            'product': product,
            'quantity': quantity,
            'total': total,
        })

    context = {
        'basket': basket_items,
        'total': basket.get_total_price(),
    }
    return render(request, 'basket_detail.html', context)

