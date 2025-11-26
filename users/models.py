from django.db import models
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage


class Profile(models.Model):
    """
    Model to store user profiles.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to='profile_pics',
        storage=S3Boto3Storage()
    )
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
