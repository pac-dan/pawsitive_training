from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

SUBSCRIPTION_CHOICES = (
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly'),
)


class Subscription(models.Model):
    """
    Model to store user subscriptions.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription")
    subscription_type = models.CharField(max_length=50, choices=SUBSCRIPTION_CHOICES, default='monthly')
    start_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Set the expiry date based on the subscription type.
        """
        # Set the expiry date based on the subscription type
        if not self.expiry_date:
            if self.subscription_type == 'monthly':
                # Add 30 days to the start date
                self.expiry_date = self.start_date + timedelta(days=30)
            elif self.subscription_type == 'yearly':
                # Add 365 days to the start date
                self.expiry_date = self.start_date + timedelta(days=365)
        super().save(*args, **kwargs)

    def is_active(self):
        """
        Check if the subscription is active.
        """
        return self.active and self.expiry_date > timezone.now()

    def __str__(self):
        """
        Return a string representation of the subscription.
        """
        return f"{self.user.username}'s Subscription"
