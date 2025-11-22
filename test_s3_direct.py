import os
import boto3
from django.conf import settings
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawsitive_training.settings')
django.setup()

print("Testing S3 upload with boto3...")

# Test direct S3 upload
s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)

# Test file
test_content = b"Test file content from Django on Heroku"
test_key = "training/videos/test_direct_upload.txt"

try:
    s3.put_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=test_key,
        Body=test_content,
        ContentType='text/plain'
    )
    print(f"✅ Direct S3 upload successful: {test_key}")

    # Check if we can retrieve it
    response = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=test_key)
    retrieved_content = response['Body'].read()
    if retrieved_content == test_content:
        print("✅ File retrieval successful")
    else:
        print("❌ File retrieval failed - content mismatch")

except Exception as e:
    print(f"❌ S3 test failed: {e}")

# Test Django storage
print("\nTesting Django storage...")
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

try:
    test_key_django = "training/videos/test_django_storage.txt"
    file_obj = ContentFile(test_content, name=test_key_django)

    # Save using Django's default storage
    saved_name = default_storage.save(test_key_django, file_obj)
    print(f"✅ Django storage save successful: {saved_name}")

    # Check if file exists
    if default_storage.exists(saved_name):
        print("✅ File exists in storage")
    else:
        print("❌ File does not exist in storage")

except Exception as e:
    print(f"❌ Django storage test failed: {e}")
    import traceback
    traceback.print_exc()
