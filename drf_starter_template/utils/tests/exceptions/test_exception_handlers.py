import json
from unittest.mock import patch

from django.test import RequestFactory
from django.test import TestCase
from django.test import override_settings
from rest_framework import status
from rest_framework.response import Response

from drf_starter_template.utils.exceptions import custom_django_page_not_found_view
from drf_starter_template.utils.exceptions import custom_django_server_error_view
from drf_starter_template.utils.exceptions import custom_drf_exception_handler


@override_settings(API_DEFAULT_VERSION="1.0", DEBUG=False)
class ExceptionHandlerTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_drf_exception_handler_with_response(self):
        # Setup a dummy DRF response that contains a 'detail' field.
        dummy_detail = "Something went wrong"
        dummy_status = status.HTTP_400_BAD_REQUEST
        dummy_response = Response({"detail": dummy_detail}, status=dummy_status)
        dummy_exc = Exception("Dummy error for testing")
        context = {"view": "dummy_view"}

        with patch(
            "drf_starter_template.utils.exceptions.exception_handler",
            return_value=dummy_response,
        ) as mock_handler:
            result = custom_drf_exception_handler(dummy_exc, context)
            expected_payload = {
                "apiVersion": "1.0",
                "error": {
                    "message": dummy_detail,
                    "code": dummy_status,
                    "extra": {"detail": dummy_detail},
                },
            }
            assert result.status_code == dummy_status
            assert result.data == expected_payload
            mock_handler.assert_called_once_with(dummy_exc, context)

    def test_drf_exception_handler_without_response(self):
        dummy_exc = Exception("Server error occurred")
        context = {"view": "dummy_view"}
        expected_status = status.HTTP_500_INTERNAL_SERVER_ERROR

        with patch(
            "drf_starter_template.utils.exceptions.exception_handler", return_value=None
        ) as mock_handler:
            result = custom_drf_exception_handler(dummy_exc, context)
            expected_payload = {
                "apiVersion": "1.0",
                "error": {
                    "message": "Internal Server Error",
                    "code": expected_status,
                    "extra": {"detail": "Unhandled exception occurred"},
                },
            }
            assert result.status_code == expected_status
            assert result.data == expected_payload
            mock_handler.assert_called_once_with(dummy_exc, context)

    def test_custom_django_page_not_found_view(self):
        request = self.factory.get("/")
        dummy_exception = Exception("Page not found error")
        response = custom_django_page_not_found_view(request, dummy_exception)

        expected_payload = {
            "apiVersion": "1.0",
            "error": {
                "message": "Resource not found",
                "code": status.HTTP_404_NOT_FOUND,
                "extra": {"detail": str(dummy_exception)},
            },
        }
        assert response.status_code == status.HTTP_404_NOT_FOUND
        content = json.loads(response.content)
        assert content == expected_payload

    def test_custom_django_server_error_view(self):
        request = self.factory.get("/")
        response = custom_django_server_error_view(request)

        expected_payload = {
            "apiVersion": "1.0",
            "error": {
                "message": "Internal Server Error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "extra": {"detail": "An unexpected error occurred on the server"},
            },
        }
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        content = json.loads(response.content)
        assert content == expected_payload

    def test_drf_exception_handler_various_drf_exceptions(self):
        from rest_framework.exceptions import AuthenticationFailed
        from rest_framework.exceptions import NotFound
        from rest_framework.exceptions import PermissionDenied
        from rest_framework.exceptions import ValidationError

        test_cases = [
            (
                ValidationError("Invalid input"),
                status.HTTP_400_BAD_REQUEST,
                "Invalid input",
            ),
            (NotFound("Not Found error"), status.HTTP_404_NOT_FOUND, "Not Found error"),
            (
                PermissionDenied("Permission denied"),
                status.HTTP_403_FORBIDDEN,
                "Permission denied",
            ),
            (
                AuthenticationFailed("Auth required"),
                status.HTTP_401_UNAUTHORIZED,
                "Auth required",
            ),
        ]
        context = {"view": "dummy_view"}
        for exc, expected_status, expected_message in test_cases:
            dummy_response = Response(
                {"detail": expected_message}, status=expected_status
            )
            with patch(
                "drf_starter_template.utils.exceptions.exception_handler",
                return_value=dummy_response,
            ) as mock_handler:
                result = custom_drf_exception_handler(exc, context)
                expected_payload = {
                    "apiVersion": "1.0",
                    "error": {
                        "message": expected_message,
                        "code": expected_status,
                        "extra": {"detail": expected_message},
                    },
                }
                assert result.status_code == expected_status
                assert result.data == expected_payload
                mock_handler.assert_called_once_with(exc, context)
