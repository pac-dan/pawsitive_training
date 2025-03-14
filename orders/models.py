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
    #  add fields such as status, shipping address, etc.
    
    def __str__(self):
        return f"Order {self.stripe_checkout_session_id} for {self.user or 'Guest'}"
