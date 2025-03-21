from django.conf import settings

def stripe_keys(request):
    return {
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
        'STRIPE_PRICE_ID_YEARLY': settings.STRIPE_PRICE_ID_YEARLY,
        'STRIPE_PRICE_ID_MONTHLY': settings.STRIPE_PRICE_ID_MONTHLY,
    }
