from django.urls import path
from . import views
from . import webhooks

app_name = 'payments'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
    path('success/', views.payment_success, name='payment-success'),
    path('cancel/', views.payment_cancel, name='payment-cancel'),
]
