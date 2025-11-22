import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawsitive_training.settings')
django.setup()

from training.models import Training
from django.core.files.storage import default_storage

print("Default storage:", type(default_storage).__name__)

# Create a training instance to check field storage
training = Training()
print("Training instance video_file field storage:", type(training.video_file.storage).__name__)
print("Training instance thumbnail field storage:", type(training.thumbnail.storage).__name__)

# Check if they are the same object
print("Same storage object?", training.video_file.storage is default_storage)
