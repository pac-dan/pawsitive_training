from django.shortcuts import render, get_object_or_404
from products.models import Product
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
from basket.models import Basket

def checkout(request):
    # Instantiate Basket object
    basket_obj = Basket(request)
    
    basket_items = []
    # Iterate over key-value pairs where key is product_id
    for product_id, item in basket_obj.basket.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = item['quantity']
        total = product.price * quantity
        basket_items.append({
            'product': product,
            'quantity': quantity,
            'total': total,
        })
        
    basket_total = basket_obj.get_total_price()
    
    context = {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'basket': basket_items,
        'basket_total': basket_total,
    }
    return render(request, 'payments/checkout.html', context)


@csrf_exempt
def create_checkout_session(request):
    domain_url = request.build_absolute_uri('/')[:-1]
    try:
        total_amount = 0  # Replace with actual basket total in cents
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Pawsitive Training Order',
                    },
                    'unit_amount': total_amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain_url + reverse('payments:payment-success'),
            cancel_url=domain_url + reverse('payments:payment-cancel'),
        )
        return JsonResponse({'id': session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)

def payment_success(request):
    basket_obj = Basket(request)
    basket_obj.clear()
    return render(request, 'payments/success.html')

def payment_cancel(request):
    return render(request, 'payments/cancel.html')