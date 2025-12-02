import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from orders.models import Order
from orders.utils import send_order_confirmation_email

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

        metadata = session.get('metadata', {})
        order_id = metadata.get('order_id')
        user_id = metadata.get('user_id')

        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.status = "paid"
                order.payment_confirmed = True

                if user_id and not order.user:
                    try:
                        user = User.objects.get(id=user_id)
                        order.user = user
                    except User.DoesNotExist:
                        print(f"User {user_id} not found")

                if session.get('shipping_details'):
                    shipping = session['shipping_details']
                    address_parts = []
                    if shipping.get('name'):
                        address_parts.append(shipping['name'])
                    addr = shipping.get('address', {})
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

                if session.get('customer_details', {}).get('email'):
                    order.customer_email = session['customer_details']['email']

                order.save()
                print(f"Updated order {order_id}")

                if order.customer_email and order.items.exists():
                    send_order_confirmation_email(order)

            except Order.DoesNotExist:
                print(f"Order {order_id} not found")
            except Exception as e:
                print(f"Error processing order: {str(e)}")
                return HttpResponse(status=400)

    return HttpResponse(status=200)
