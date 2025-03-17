from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

SUBSCRIPTION_CHOICES = (
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly'),
)

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription")
    subscription_type = models.CharField(max_length=50, choices=SUBSCRIPTION_CHOICES, default='monthly')
    start_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # If expiry_date is not set, calculate it based on subscription type.
        if not self.expiry_date:
            if self.subscription_type == 'monthly':
                self.expiry_date = self.start_date + timedelta(days=30)
            elif self.subscription_type == 'yearly':
                self.expiry_date = self.start_date + timedelta(days=365)
        super().save(*args, **kwargs)

    def is_active(self):
        return self.active and self.expiry_date > timezone.now()

    def __str__(self):
        return f"{self.user.username}'s Subscription"
