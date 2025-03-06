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
    new_quantity = basket.basket[str(product_id_str)]['quantity']
    
    data = {
        'grand_total': str(basket.get_total_price()),
        'basket_items': len(basket),
        'product_id': product.id, 
        'product_quantity': new_quantity,
    }
    return JsonResponse(data)

@require_POST
def basket_remove(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Remove one unit of the product (or the entire product if quantity == 1)
    basket.remove(product)
    
    product_id_str = str(product.id)
    # Get the updated quantity; if the product is no longer in the basket, return 0.
    new_quantity = basket.basket.get(product_id_str, {}).get('quantity', 0)
    
    data = {
        'grand_total': str(basket.get_total_price()),
        'basket_items': len(basket),
        'product_id': product.id,
        'product_quantity': new_quantity,
    }
    return JsonResponse(data)

# The basket_detail view retrieves the current basket from the session and renders the basket detail template.
def basket_detail(request):
    basket = Basket(request)
    return render(request, 'basket_detail.html', {'basket': basket})

