import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    """
    A view to handle the Stripe webhooks
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET_PAYMENTS

    # Verify the event by constructing it from the payload and signature
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)  # Invalid payload
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)  # Invalid signature

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # 1) Extract the user_id from metadata
        user_id = session.get('metadata', {}).get('user_id')  
        # 2) Convert from cents to dollars
        amount = session.get('amount_total', 0) / 100.0

        from orders.models import Order
        order, created = Order.objects.get_or_create(
            stripe_checkout_session_id=session['id'],
            defaults={'amount': amount, 'user': None}
        )

        # 3) If we have a user_id, attach it to the Order
        if user_id:
            from django.contrib.auth.models import User
            try:
                user = User.objects.get(id=user_id)
                order.user = user
                order.save()
            except User.DoesNotExist:
                pass

        # 4) Update the order status to 'paid'
        metadata = session.get('metadata', {})
        order_id = metadata.get('order_id')        
        if order_id:
            order = Order.objects.get(id=order_id)
            order.status = "paid"
            order.save()

    return HttpResponse(status=200)


