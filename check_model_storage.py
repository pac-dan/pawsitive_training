import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawsitive_training.settings')
django.setup()

from training.models import Training
from django.core.files.storage import default_storage

print("Default storage:", type(default_storage).__name__)
print("Training.video_file.storage:", type(Training.video_file.storage).__name__)
print("Training.thumbnail.storage:", type(Training.thumbnail.storage).__name__)

# Check if they are the same object
print("Same storage object?", Training.video_file.storage is default_storage)
