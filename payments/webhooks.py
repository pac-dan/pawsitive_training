import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)  # Invalid payload
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)  # Invalid signature

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Extract metadata; values in metadata are strings.
        user_id = session.get('metadata', {}).get('user_id')
        # Stripe returns the amount in cents. Convert it to dollars.
        amount = session.get('amount_total', 0) / 100.0

        # Import the Order model (adjust the import path as needed)
        from orders.models import Order
        order, created = Order.objects.get_or_create(
            stripe_checkout_session_id=session['id'],
            defaults={'amount': amount, 'user': None}
        )

        if user_id:
            try:
                from django.contrib.auth.models import User
                user = User.objects.get(id=user_id)
                order.user = user
                order.save()
            except User.DoesNotExist:
                pass

        # Add more fields to the Order model as needed
        print("Payment completed successfully! Order created.")

    return HttpResponse(status=200)

