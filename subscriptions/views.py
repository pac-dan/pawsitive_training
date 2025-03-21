from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Subscription
import stripe 
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
from orders.models import Order
import uuid

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def subscribe(request):
    try:
        subscription = request.user.subscription
    except Subscription.DoesNotExist:
        subscription = None

    context = {'subscription': subscription}
    return render(request, 'subscriptions/subscribe.html', context)

@login_required
def create_subscription_checkout(request):
    domain_url = request.build_absolute_uri('/')[:-1]
    price_id = request.GET.get('price_id')
    
    if not price_id:
        return JsonResponse({'error': 'No Price ID provided.'}, status=400)
    
    try:
        user_id_str = str(request.user.id)
        # Create an order record for this subscription purchase
        order = Order.objects.create(
            user=request.user,
            stripe_checkout_session_id=str(uuid.uuid4()),  # Use a temporary unique value for now
            amount=250 if price_id == settings.STRIPE_PRICE_ID_YEARLY else 50,
            status="pending"
        )
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            # Pass metadata including the Order's primary key as 'order_id'
            metadata={'user_id': user_id_str, 'order_id': str(order.id)},
            subscription_data={
                'metadata': {'user_id': user_id_str, 'order_id': str(order.id)}
            },
            client_reference_id=user_id_str,
            success_url=domain_url + reverse('subscriptions:subscription_success'),
            cancel_url=domain_url + reverse('subscriptions:subscribe'),
        )
        return JsonResponse({'id': session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)

@login_required
def subscription_success(request):
    """
    Renders a success page after a successful subscription purchase.
    Note: In production, subscription status should be updated via Stripe webhooks.
    """
    return render(request, 'subscriptions/success.html')

@csrf_exempt
def stripe_subscription_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET_SUBSCRIPTIONS

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        print("Webhook event received:", event['type'])
        print("Full event payload:", event)  # This will show all data, including metadata.
    except ValueError as e:
        print("Invalid payload:", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print("Invalid signature:", e)
        return HttpResponse(status=400)

    if event['type'] in ['customer.subscription.created', 'customer.subscription.updated']:
        subscription_event = event['data']['object']
        metadata = subscription_event.get('metadata', {})
        user_id = metadata.get('user_id')
        order_id = metadata.get('order_id')
        print("Metadata from event:", metadata)
        print("Processing subscription event for user_id:", user_id)
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                sub, created = Subscription.objects.get_or_create(user=user)
                sub.stripe_subscription_id = subscription_event['id']
                sub.active = True
                sub.start_date = timezone.now()
                sub.expiry_date = timezone.now() + timedelta(days=30)
                sub.save()
                print("Subscription updated for user:", user.username)
                if order_id:
                # Update the corresponding order record
                    order = Order.objects.get(id=order_id)
                    order.status = "paid"  # Mark as paid or complete
                    order.save()
                print("Order updated for order_id:", order_id)
            except Exception as e:
                print("Error updating subscription for user_id {}: {}".format(user_id, e))
    elif event['type'] == 'customer.subscription.deleted':
        subscription_event = event['data']['object']
        user_id = subscription_event.get('metadata', {}).get('user_id')
        print("Processing deletion event for user_id:", user_id)
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                sub = user.subscription
                sub.active = False
                sub.save()
                print("Subscription deactivated for user:", user.username)
            except Exception as e:
                print("Error deactivating subscription for user_id {}: {}".format(user_id, e))

    return HttpResponse(status=200)

@csrf_exempt
def stripe_payments_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET_PAYMENTS

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        print("Payments webhook event received:", event['type'])
    except ValueError as e:
        print("Invalid payload:", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print("Invalid signature:", e)
        return HttpResponse(status=400)

    # Process the payment event here...
    return HttpResponse(status=200)
