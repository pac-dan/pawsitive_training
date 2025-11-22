import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawsitive_training.settings')

# Let's check what happens before Django setup
print("Before Django setup:")
print("DEFAULT_FILE_STORAGE in env:", os.environ.get('DEFAULT_FILE_STORAGE'))

# Now setup Django
django.setup()

from django.conf import settings
import environ

print("\nAfter Django setup:")
print("DEBUG:", settings.DEBUG)
print("DEFAULT_FILE_STORAGE:", settings.DEFAULT_FILE_STORAGE)

# Check if storages is imported
try:
    import storages
    print("storages module imported successfully")
except ImportError as e:
    print("storages import failed:", e)

# Check env loading
env = environ.Env()
print("AWS_ACCESS_KEY_ID from env():", env('AWS_ACCESS_KEY_ID'))
print("AWS_STORAGE_BUCKET_NAME from env():", env('AWS_STORAGE_BUCKET_NAME'))

# Let's manually set what should be set
print("\nManual S3 config check:")
if not settings.DEBUG:
    print("Should be setting S3 config since DEBUG=False")
    try:
        test_storage = 'storages.backends.s3boto3.S3Boto3Storage'
        print(f"Test storage string: {test_storage}")
        # Try to import it
        from storages.backends.s3boto3 import S3Boto3Storage
        print("S3Boto3Storage imported successfully")
    except Exception as e:
        print(f"S3Boto3Storage import failed: {e}")
else:
    print("DEBUG=True, so not setting S3 config")
