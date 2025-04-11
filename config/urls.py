#!/usr/bin/env python
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls import handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import reverse_lazy
from django.views import debug as debug_views
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView

from drf_starter_template.users.views import LoginApi
from drf_starter_template.utils.exceptions import custom_django_page_not_found_view
from drf_starter_template.utils.exceptions import custom_django_server_error_view

if settings.DEBUG:
    debug_views.technical_404_response = custom_django_page_not_found_view
    debug_views.technical_500_response = custom_django_server_error_view
else:
    handler404 = custom_django_page_not_found_view
    handler500 = custom_django_server_error_view


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # App-specific URLs
    path("users/", include("drf_starter_template.users.urls", namespace="users")),
    path(
        "examples/",
        include("drf_starter_template.examples.urls", namespace="examples"),
    ),
    # Root routes
    path("auth/login/", LoginApi.as_view(), name="api-login"),
    # API Schema
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Redirect root to the Swagger UI
    path("", RedirectView.as_view(url=reverse_lazy("swagger-ui"), permanent=False)),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

# Django Debug Toolbar URLs in debug mode
if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
