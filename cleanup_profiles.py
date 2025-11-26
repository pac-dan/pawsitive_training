#!/usr/bin/env python
"""
Temporary script to clean up profile images with default.jpg
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawsitive_training.settings')
django.setup()

from users.models import Profile

# Update profiles with default.jpg to None
count = Profile.objects.filter(image='default.jpg').update(image=None)
print(f'Updated {count} profile(s) with default.jpg to None')

# Check for empty string images too
count2 = Profile.objects.filter(image='').update(image=None)
print(f'Updated {count2} profile(s) with empty string to None')

print('\n--- Current Profile Image Status ---')
total = Profile.objects.count()
with_images = Profile.objects.exclude(image__isnull=True).exclude(image='').count()
without_images = Profile.objects.filter(image__isnull=True).count() + Profile.objects.filter(image='').count()

print(f'Total profiles: {total}')
print(f'With images: {with_images}')
print(f'Without images: {without_images}')

