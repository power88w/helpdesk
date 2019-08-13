from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Create Static folder and store all files there"""
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """Keep Media files in separate folder"""
    location = settings.MEDIAFILES_LOCATION