import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawsitive_training.settings')
django.setup()

from django.core.files.storage import default_storage

print("Default storage type:", type(default_storage))
print("Default storage backend:", default_storage.__class__.__name__)
print("Default storage backend module:", default_storage.__class__.__module__)

# Check if it's actually S3
if hasattr(default_storage, 'bucket_name'):
    print("Bucket name:", default_storage.bucket_name)
if hasattr(default_storage, 'location'):
    print("Location:", default_storage.location)

# Check the actual backend
if hasattr(default_storage, 'backend'):
    print("Backend:", type(default_storage.backend))
    print("Backend class:", default_storage.backend.__class__.__name__)
else:
    print("No backend attribute")

# Let's also check what storage the field actually gets
from training.models import Training
training = Training()
field_storage = training.video_file.storage
print("\nField storage type:", type(field_storage))
print("Field storage class:", field_storage.__class__.__name__)
print("Field storage module:", field_storage.__class__.__module__)

if hasattr(field_storage, 'bucket_name'):
    print("Field bucket name:", field_storage.bucket_name)
