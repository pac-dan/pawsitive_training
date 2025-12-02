import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
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
        print("Payments webhook event received:", event['type'])
    except ValueError as e:
        print("Invalid payload:", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print("Invalid signature:", e)
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print("Processing checkout.session.completed event")

        # Get metadata from the session
        metadata = session.get('metadata', {})
        order_id = metadata.get('order_id')
        user_id = metadata.get('user_id')

        if order_id:
            try:
                # Find and update the order
                order = Order.objects.get(id=order_id)
                order.status = "paid"
                order.save()
                print(f"Updated order {order_id} status to paid")

                # If we have a user_id, make sure the order is attached to the user
                if user_id and not order.user:
                    try:
                        user = User.objects.get(id=user_id)
                        order.user = user
                        order.save()
                    except User.DoesNotExist:
                        print(f"User {user_id} not found")
            except Order.DoesNotExist:
                print(f"Order {order_id} not found")
            except Exception as e:
                print(f"Error processing order: {str(e)}")
                return HttpResponse(status=400)

    return HttpResponse(status=200)
