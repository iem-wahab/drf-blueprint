from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework.views import exception_handler


def custom_drf_exception_handler(exc, context):
    drf_response = exception_handler(exc, context)
    if drf_response is not None:
        status_code = drf_response.status_code
        data = drf_response.data

        user_message, extra = extract_error_details(data, exc)
        drf_response.data = _build_error_payload(user_message, status_code, extra)
        return drf_response

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Internal Server Error"
    extra = {"detail": "Unhandled exception occurred"}
    return Response(
        _build_error_payload(message, status_code, extra), status=status_code
    )


def custom_django_page_not_found_view(request, exception):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Resource not found"
    extra = {"detail": str(exception)}
    return JsonResponse(
        _build_error_payload(message, status_code, extra), status=status_code
    )


def custom_django_server_error_view(request):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Internal Server Error"
    extra = {"detail": "An unexpected error occurred on the server"}
    return JsonResponse(
        _build_error_payload(message, status_code, extra), status=status_code
    )


def _build_error_payload(message, code, extra):
    return {
        "apiVersion": settings.API_DEFAULT_VERSION,
        "error": {
            "message": message,
            "code": code,
            "extra": extra,
        },
    }


def extract_error_details(data, exc):
    if isinstance(data, dict):
        if "detail" in data:
            return _process_detail(data["detail"], exc)
        first_key = next(iter(data))
        val = data[first_key]
        if isinstance(val, list):
            user_message = str(val[0]) if val else str(exc)
        elif isinstance(val, (dict, ReturnDict)):
            user_message, _ = extract_error_details(val, exc)
        else:
            user_message = str(val)
        return user_message, data
    if isinstance(data, list):
        return (str(data[0]) if data else str(exc)), {"detail": data}
    return str(data or exc), {}


def _process_detail(detail, exc):
    if isinstance(detail, (list, ReturnList)):
        user_message = str(detail[0]) if detail else str(exc)
        return user_message, {"detail": detail}
    if isinstance(detail, (dict, ReturnDict)):
        first_key = next(iter(detail))
        first_val = detail[first_key]
        if isinstance(first_val, list):
            user_message = str(first_val[0]) if first_val else str(exc)
        else:
            user_message = str(first_val)
        return user_message, {"detail": detail}
    return str(detail), {"detail": detail}
