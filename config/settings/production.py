#!/usr/bin/env python


from config.env import env

from .common import Common


class Production(Common):
    # Inherit base installed apps
    INSTALLED_APPS = Common.INSTALLED_APPS
    # Production secret key
    SECRET_KEY = env(
        "DJANGO_SECRET_KEY", default="production-need-real-key-in-production"
    )

    # Allowed Hosts
    ALLOWED_HOSTS = ["*"]

    # Production WSGI Server - Gunicorn configuration
    INSTALLED_APPS += ("gunicorn",)

    # Disable debugging
    DEBUG = False

    # Email
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    # Static & Media Files
    INSTALLED_APPS += ("storages",)
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID = env("DJANGO_AWS_ACCESS_KEY_ID", default="")
    AWS_SECRET_ACCESS_KEY = env("DJANGO_AWS_SECRET_ACCESS_KEY", default="")
    AWS_STORAGE_BUCKET_NAME = env("DJANGO_AWS_STORAGE_BUCKET_NAME", default="")
    AWS_DEFAULT_ACL = "public-read"
    AWS_AUTO_CREATE_BUCKET = True
    AWS_QUERYSTRING_AUTH = False
    MEDIA_URL = f"https://s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/"

    AWS_HEADERS = {
        "Cache-Control": "max-age=86400, s-maxage=86400, must-revalidate",
    }
