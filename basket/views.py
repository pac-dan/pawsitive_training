from django.shortcuts import get_object_or_404, render, redirect
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

    # Get quantity from request body (for product detail pages) or default to 1
    quantity = int(request.POST.get('quantity', 1))

    # Validate quantity
    if quantity <= 0:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'error': 'Quantity must be greater than 0.'
            }, status=400)
        else:
            from django.contrib import messages
            messages.error(request, 'Quantity must be greater than 0.')
            return redirect('basket_detail')

    # Check stock availability
    if quantity > product.stock:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'error': f'Only {product.stock} items available in stock.'
            }, status=400)
        else:
            from django.contrib import messages
            messages.error(request, f'Only {product.stock} items available in stock.')
            return redirect('basket_detail')

    basket.add(product=product, quantity=quantity, update_quantity=False)

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
        'message': f'{quantity} item(s) added to basket successfully!'
    }

    # If it's an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(data)

    # If it's a regular form submission, redirect to basket with success message
    from django.contrib import messages
    messages.success(request, f'{quantity} item(s) added to basket successfully!')
    return redirect('basket_detail')


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


@require_POST
def basket_update(request, product_id):
    """
    A view to update the quantity of a product in the shopping basket.
    """
    try:
        # Get the quantity from the request
        quantity = int(request.POST.get('quantity', 1))

        # Validate quantity
        if quantity <= 0:
            # If quantity is 0 or negative, remove the item
            basket = Basket(request)
            product = get_object_or_404(Product, id=product_id)

            # Remove the product completely
            product_id_str = str(product.id)
            if product_id_str in basket.basket:
                del basket.basket[product_id_str]
                basket.save()

            data = {
                'grand_total': str(basket.get_total_price()),
                'basket_items': len(basket),
                'product_id': product.id,
                'product_quantity': 0,
                'product_price': str(product.price),
                'line_total': '0.00',
                'message': 'Product removed from basket.'
            }

            return JsonResponse(data)

        # Check stock availability
        product = get_object_or_404(Product, id=product_id)
        if quantity > product.stock:
            return JsonResponse({
                'error': f'Only {product.stock} items available in stock.'
            }, status=400)

        # Update the basket
        basket = Basket(request)
        basket.add(product=product, quantity=quantity, update_quantity=True)

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
            'product_price': str(product_price),
            'line_total': str(line_total),
            'message': 'Basket updated successfully!'
        }

        return JsonResponse(data)

    except ValueError:
        return JsonResponse({
            'error': 'Invalid quantity provided.'
        }, status=400)
    except Exception:
        return JsonResponse({
            'error': 'An error occurred while updating the basket.'
        }, status=500)


def basket_info(request, product_id):
    """
    A view to get basket information for a specific product.
    """
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)

    product_id_str = str(product.id)
    current_quantity = basket.basket.get(product_id_str, {}).get('quantity', 0)

    data = {
        'product_id': product.id,
        'current_quantity': current_quantity,
        'available_stock': product.stock,
        'can_add_more': current_quantity < product.stock
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
