from django.conf import settings
from drf_spectacular.openapi import AutoSchema


class CustomAutoSchema(AutoSchema):
    def get_serializer_name(self, serializer, direction):
        try:
            name = serializer.__qualname__
        except AttributeError:
            name = serializer.__class__.__name__
        name = name.replace(".", "_")
        view_name = self.view.__class__.__name__
        if view_name not in name:
            name = f"{view_name}_{name}"
        return name


def format_schema_response(result, generator, request, public):
    for path_item in result.get("paths", {}).values():
        for operation in path_item.values():
            responses = operation.get("responses", {})
            for status_code, response in responses.items():
                content = response.get("content", {})
                app_json = content.get("application/json", {})
                if not app_json:
                    continue
                original_schema = app_json.get("schema", {})
                if status_code.startswith("2"):
                    app_json["schema"] = {
                        "type": "object",
                        "properties": {
                            "apiVersion": {
                                "type": "string",
                                "example": settings.API_DEFAULT_VERSION,
                            },
                            "data": original_schema,
                        },
                        "required": ["apiVersion", "data"],
                    }
                else:
                    app_json["schema"] = {
                        "type": "object",
                        "properties": {
                            "apiVersion": {
                                "type": "string",
                                "example": settings.API_DEFAULT_VERSION,
                            },
                            "error": original_schema,
                        },
                        "required": ["apiVersion", "error"],
                    }
                response["content"]["application/json"] = app_json
    return result


def custom_preprocessing_hook(endpoints):
    filtered = []
    for path, path_regex, method, callback in endpoints:
        if "schema" not in path:
            filtered.append((path, path_regex, method, callback))
    return filtered
