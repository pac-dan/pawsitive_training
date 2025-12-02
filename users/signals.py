from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


# This receiver listens for the post_save signal from the User model.
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create the profile for new users
        Profile.objects.create(user=instance)
    else:
        # For existing users, check if profile exists; if not, create it.
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)
        else:
            instance.profile.save()
