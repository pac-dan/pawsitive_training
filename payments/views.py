from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages
import stripe
import uuid
from basket.models import Basket
from orders.models import Order, OrderItem
from orders.utils import send_order_confirmation_email

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    """
    A view to return the checkout page.
    """
    basket_obj = Basket(request)

    # Check if basket is empty
    if len(basket_obj.basket) == 0:
        messages.warning(request, 'Your basket is empty. Please add some items before checking out.')
        return redirect('products:products_display')

    # Check if Stripe is configured
    if not settings.STRIPE_PUBLISHABLE_KEY:
        messages.error(request, 'Payment system is not configured. Please contact support.')
        return redirect('basket_detail')

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


def create_checkout_session(request):
    """
    A view to create a new Checkout Session using the Stripe API.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    # Check if Stripe is configured
    if not settings.STRIPE_SECRET_KEY or not settings.STRIPE_PUBLISHABLE_KEY:
        return JsonResponse(
            {'error': 'Payment system is not configured. Please contact support.'},
            status=500
        )

    domain_url = request.build_absolute_uri('/')[:-1]
    try:
        basket_obj = Basket(request)
        basket_total = int(basket_obj.get_total_price() * 100)

        # Create an order record for this purchase
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            stripe_checkout_session_id=str(uuid.uuid4()),
            amount=basket_obj.get_total_price(),
            status="pending"
        )

        metadata = {}
        if request.user.is_authenticated:
            metadata['user_id'] = request.user.id
        # Use the primary key as the order identifier
        metadata['order_id'] = str(order.id)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Pawsitive Training Order',
                    },
                    'unit_amount': basket_total,
                },
                'quantity': 1,
            }],
            mode='payment',
            shipping_address_collection={
                'allowed_countries': ['US', 'GB', 'IE']
            },
            success_url=domain_url + reverse('payments:payment-success') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url + reverse('payments:payment-cancel'),
            metadata=metadata,
        )
        return JsonResponse({'id': session.id, 'message': 'Redirecting to payment gateway...'})
    except Exception as e:
        return JsonResponse(
            {'error': str(e), 'message': 'There was an error creating the checkout session.'},
            status=403
        )


def payment_success(request):
    """
    A view to handle a successful payment.
    """
    session_id = request.GET.get('session_id')
    order = None

    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(
                session_id,
                expand=['customer', 'shipping_details']
            )

            order_id = session.metadata.get('order_id')
            if order_id:
                order = Order.objects.get(id=order_id)

                if not order.payment_confirmed:
                    basket_obj = Basket(request)

                    for item in basket_obj:
                        product = item['product']
                        quantity = item['quantity']

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            price=product.price
                        )

                        product.stock = max(product.stock - quantity, 0)
                        product.save()

                    if session.shipping_details:
                        address_parts = []
                        if session.shipping_details.get('name'):
                            address_parts.append(session.shipping_details['name'])
                        addr = session.shipping_details.get('address', {})
                        if addr.get('line1'):
                            address_parts.append(addr['line1'])
                        if addr.get('line2'):
                            address_parts.append(addr['line2'])
                        if addr.get('city'):
                            address_parts.append(addr['city'])
                        if addr.get('state'):
                            address_parts.append(addr['state'])
                        if addr.get('postal_code'):
                            address_parts.append(addr['postal_code'])
                        if addr.get('country'):
                            address_parts.append(addr['country'])

                        order.shipping_address = '\n'.join(address_parts)

                    order.customer_email = session.customer_details.get('email', '')
                    order.payment_confirmed = True
                    order.status = 'paid'
                    order.save()

                    send_order_confirmation_email(order)
                    basket_obj.clear()

        except Exception as e:
            print(f"Error processing payment success: {e}")

    messages.success(request, "Your payment was successful and your order has been placed!")
    return render(request, 'payments/success.html', {'order': order})


def payment_cancel(request):
    """
    A view to handle a cancelled payment.
    """
    messages.error(request, "Your payment was cancelled. Please try again.")
    return render(request, 'payments/cancel.html')
