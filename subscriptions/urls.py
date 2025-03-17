from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),  # Existing subscription page
    path('purchase/', views.create_subscription_checkout, name='purchase'),
    path('success/', views.subscription_success, name='subscription_success'),
    path('webhook/', views.stripe_subscription_webhook, name='stripe_subscription_webhook'),
]