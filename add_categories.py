#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawsitive_training.settings')
django.setup()

from products.models import ProductCategory
from training.models import TrainingCategory

# Create Product Categories
product_cats = [
    {'name': 'Training Equipment', 'slug': 'training-equipment'},
    {'name': 'Toys', 'slug': 'toys'},
    {'name': 'Food & Treats', 'slug': 'food-treats'},
    {'name': 'Accessories', 'slug': 'accessories'},
    {'name': 'Health & Wellness', 'slug': 'health-wellness'},
]

print("Creating Product Categories...")
for cat in product_cats:
    obj, created = ProductCategory.objects.get_or_create(
        slug=cat['slug'],
        defaults={'name': cat['name']}
    )
    if created:
        print(f"✅ Created: {cat['name']}")
    else:
        print(f"⚠️  Already exists: {cat['name']}")

# Create Training Categories
training_cats = [
    {'name': 'Beginner Training', 'slug': 'beginner'},
    {'name': 'Intermediate Training', 'slug': 'intermediate'},
    {'name': 'Advanced Training', 'slug': 'advanced'},
    {'name': 'Behavior & Obedience', 'slug': 'behavior-obedience'},
    {'name': 'Tricks & Fun', 'slug': 'tricks-fun'},
]

print("\nCreating Training Categories...")
for tcat in training_cats:
    obj, created = TrainingCategory.objects.get_or_create(
        slug=tcat['slug'],
        defaults={'name': tcat['name']}
    )
    if created:
        print(f"✅ Created: {tcat['name']}")
    else:
        print(f"⚠️  Already exists: {tcat['name']}")

print("\n✅ All categories created successfully!")

