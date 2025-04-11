#!/usr/bin/env python

from pathlib import Path

from configurations import Configuration

from config.env import env

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment
env.read_env(BASE_DIR.parent / ".env")


class Common(Configuration):
    INSTALLED_APPS = (
        # Django built-in apps
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # Django REST Framework and related packages
        "rest_framework",
        "rest_framework.authtoken",
        "django_filters",
        # API Documentation
        "drf_spectacular",
        # Project-specific apps
        "drf_starter_template.users",
        "drf_starter_template.core",
        "drf_starter_template.utils",
        "drf_starter_template.examples",
    )

    MIDDLEWARE = (
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    )

    ROOT_URLCONF = "config.urls"
    WSGI_APPLICATION = "config.wsgi.application"

    # Email
    ADMINS = (("Author", "admin@example.com"),)

    # General
    APPEND_SLASH = True
    TIME_ZONE = "UTC"
    LANGUAGE_CODE = "en-us"
    USE_I18N = False
    USE_L10N = True
    USE_TZ = True
    LOGIN_REDIRECT_URL = "/"

    # Static files (CSS, JavaScript, Images)
    STATIC_ROOT = Path(BASE_DIR.parent / "static").as_posix()
    STATICFILES_DIRS = []
    STATIC_URL = "/static/"
    STATICFILES_FINDERS = (
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    )

    # Media files
    MEDIA_ROOT = (BASE_DIR.parent / "media").as_posix()
    MEDIA_URL = "/media/"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": STATICFILES_DIRS,
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    # Password Validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": (
                "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
            ),
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]

    # Logging
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "django.server": {
                "()": "django.utils.log.ServerFormatter",
                "format": "[%(server_time)s] %(message)s",
            },
            "verbose": {
                "format": (
                    "%(levelname)s %(asctime)s %(module)s %(process)d "
                    "%(thread)d %(message)s"
                ),
            },
            "simple": {
                "format": "%(levelname)s %(message)s",
            },
        },
        "filters": {
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            },
        },
        "handlers": {
            "django.server": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "django.server",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "propagate": True,
            },
            "django.server": {
                "handlers": ["django.server"],
                "level": "INFO",
                "propagate": False,
            },
            "django.request": {
                "handlers": ["mail_admins", "console"],
                "level": "ERROR",
                "propagate": False,
            },
            "django.db.backends": {
                "handlers": ["console"],
                "level": "INFO",
            },
        },
    }

    # Custom user app
    AUTH_USER_MODEL = "users.User"

    # Django Rest Framework
    REST_FRAMEWORK = {
        "EXCEPTION_HANDLER": "drf_starter_template.utils.exceptions.custom_drf_exception_handler",
        "DEFAULT_PAGINATION_CLASS": "drf_starter_template.utils.pagination.CustomDRFPagination",
        "PAGE_SIZE": int(env("DJANGO_PAGINATION_LIMIT", default="10")),
        "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
        "DEFAULT_RENDERER_CLASSES": (
            "drf_starter_template.utils.renderer.CustomDRFJSONRenderer",
        ),
        "DEFAULT_PARSER_CLASSES": (
            "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        ),
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.IsAuthenticated",
        ],
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework.authentication.TokenAuthentication",
        ),
        "DEFAULT_SCHEMA_CLASS": "drf_starter_template.utils.schema.CustomAutoSchema",
        "NON_FIELD_ERRORS_KEY": "general",
    }

    # Database - SQLite for all environments
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": (BASE_DIR.parent / "db.sqlite3").as_posix(),
        },
    }

    # drf-spectacular settings
    SPECTACULAR_SETTINGS = {
        "TITLE": "DRF-Starter-Template API",
        "DESCRIPTION": "API documentation for DRF-Starter-Template",
        "VERSION": "1.0.0",
        "PARSER_WHITELIST": ["rest_framework.parsers.JSONParser"],
        "POSTPROCESSING_HOOKS": [
            "drf_starter_template.utils.schema.format_schema_response",
            "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
        ],
        "CAMELIZE_NAMES": True,
        "DEFAULT_AUTO_SCHEMA_CLASS": "drf_starter_template.utils.schema.CustomAutoSchema",
        "PREPROCESSING_HOOKS": [
            "drf_starter_template.utils.schema.custom_preprocessing_hook"
        ],
    }

    # Error handling for API requests
    DEFAULT_EXCEPTION_REPORTER_FILTER = "django.views.debug.SafeExceptionReporterFilter"

    # Default API version for consistent responses
    API_DEFAULT_VERSION = "1.0"
