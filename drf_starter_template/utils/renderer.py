from django.conf import settings
from djangorestframework_camel_case.render import CamelCaseJSONRenderer


class CustomDRFJSONRenderer(CamelCaseJSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict) and data.get("error") is not None:
            return super().render(data, accepted_media_type, renderer_context)

        if isinstance(data, dict) and "data" in data:
            response_data = data
        else:
            response_data = {"data": data}

        response_data["apiVersion"] = settings.API_DEFAULT_VERSION

        return super().render(response_data, accepted_media_type, renderer_context)
