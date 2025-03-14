from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# This receiver listens for the post_save signal from the User model.
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # When a new User is created, create a Profile for that user.
        Profile.objects.create(user=instance)
    else:
        # When an existing User is updated, save the Profile.
        instance.profile.save()
