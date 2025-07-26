from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )
    stripe_checkout_session_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")
    
    # Payment tracking
    payment_confirmed = models.BooleanField(default=False, help_text="Set to True when payment is confirmed via webhook")
    
    # Shipping information
    shipping_address = models.TextField(blank=True, null=True, help_text="Full shipping address")
    billing_address = models.TextField(blank=True, null=True, help_text="Full billing address")
    
    # Additional costs
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Order fulfillment
    shipped = models.BooleanField(default=False)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Order {self.stripe_checkout_session_id} for {self.user or 'Guest'}"
    
    @property
    def total_amount(self):
        """Calculate total amount including shipping and tax"""
        return self.amount + self.shipping_cost + self.tax_amount
