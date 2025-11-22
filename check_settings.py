import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawsitive_training.settings')
django.setup()

from django.conf import settings

print("DEBUG:", settings.DEBUG)
print("DEFAULT_FILE_STORAGE:", settings.DEFAULT_FILE_STORAGE)
print("AWS_ACCESS_KEY_ID:", getattr(settings, 'AWS_ACCESS_KEY_ID', 'NOT_SET'))
print("AWS_STORAGE_BUCKET_NAME:", getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'NOT_SET'))
print("AWS_S3_REGION_NAME:", getattr(settings, 'AWS_S3_REGION_NAME', 'NOT_SET'))
print("AWS_QUERYSTRING_AUTH:", getattr(settings, 'AWS_QUERYSTRING_AUTH', 'NOT_SET'))
