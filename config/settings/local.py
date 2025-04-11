#!/usr/bin/env python

from pathlib import Path

from config.env import env

from .common import Common

BASE_DIR = Path(__file__).resolve().parent.parent


class Local(Common):
    # Debugging
    DEBUG = True

    # Secret key
    SECRET_KEY = env(
        "DJANGO_SECRET_KEY",
        default="django-insecure-development-key-for-local-use-only",
    )

    # Allowed Hosts
    ALLOWED_HOSTS = ["*"]

    # Installed Apps
    INSTALLED_APPS = (*Common.INSTALLED_APPS, "debug_toolbar")

    # Middleware
    MIDDLEWARE = (
        *Common.MIDDLEWARE,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )

    # Debug Toolbar IPs
    INTERNAL_IPS = ["127.0.0.1", "localhost"]

    # Email
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
