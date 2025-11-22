#!/usr/bin/env python
"""
Test script to verify S3 upload works from Heroku
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawsitive_training.settings')
django.setup()

import boto3
from django.conf import settings
from io import BytesIO

print("=" * 50)
print("Testing S3 Upload Connection")
print("=" * 50)

print(f"\nBucket: {settings.AWS_STORAGE_BUCKET_NAME}")
print(f"Region: {settings.AWS_S3_REGION_NAME}")
print(f"Access Key: {settings.AWS_ACCESS_KEY_ID[:10]}...")

try:
    # Create S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    print("\n✅ S3 client created successfully")
    
    # Try to list bucket
    print("\nTesting ListBucket permission...")
    response = s3_client.list_objects_v2(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Prefix='training/videos/',
        MaxKeys=5
    )
    print(f"✅ ListBucket works! Found {response.get('KeyCount', 0)} objects")
    
    # Try to upload a test file
    print("\nTesting PutObject permission...")
    test_content = b"This is a test file from Heroku"
    test_key = "training/videos/test_upload.txt"
    
    s3_client.put_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=test_key,
        Body=BytesIO(test_content),
        ACL='public-read',
        ContentType='text/plain'
    )
    print(f"✅ Upload successful! Test file created at: {test_key}")
    
    # Try to read it back
    print("\nTesting GetObject permission...")
    obj = s3_client.get_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=test_key
    )
    content = obj['Body'].read()
    print(f"✅ Read successful! Content: {content.decode()}")
    
    # Clean up test file
    print("\nCleaning up test file...")
    s3_client.delete_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=test_key
    )
    print("✅ Test file deleted")
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED! S3 is working correctly!")
    print("=" * 50)
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

