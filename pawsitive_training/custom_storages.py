"""
Custom storage backends for AWS S3
"""
from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    """
    Storage backend for public media files that returns direct URLs
    without query string authentication.
    """
    querystring_auth = False
    default_acl = 'public-read'
    file_overwrite = False
    object_parameters = {
        'CacheControl': 'max-age=86400',
        'ContentDisposition': 'inline',
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Force querystring_auth to False to get direct public URLs
        self.querystring_auth = False

