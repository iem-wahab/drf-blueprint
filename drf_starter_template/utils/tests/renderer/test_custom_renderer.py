import json

from django.test import TestCase
from django.test import override_settings

from drf_starter_template.utils.renderer import CustomDRFJSONRenderer


@override_settings(API_DEFAULT_VERSION="1.0")
class CustomDRFJSONRendererTests(TestCase):
    def setUp(self):
        self.renderer = CustomDRFJSONRenderer()

    def get_rendered_output(self, data, renderer_context=None):
        rendered_bytes = self.renderer.render(data, renderer_context=renderer_context)
        return json.loads(rendered_bytes.decode("utf-8"))

    def test_render_error_payload(self):
        input_data = {"error": {"message_text": "error occurred", "error_code": 400}}
        expected_output = {"error": {"messageText": "error occurred", "errorCode": 400}}
        output = self.get_rendered_output(input_data)
        assert output == expected_output

    def test_render_with_existing_data_key(self):
        input_data = {"data": {"first_name": "John", "last_name": "Doe"}}
        expected_output = {
            "data": {"firstName": "John", "lastName": "Doe"},
            "apiVersion": "1.0",
        }
        output = self.get_rendered_output(input_data)
        assert output == expected_output

    def test_render_non_dict_input(self):
        input_data = [{"first_name": "Alice"}, {"first_name": "Bob"}]
        expected_output = {
            "data": [{"firstName": "Alice"}, {"firstName": "Bob"}],
            "apiVersion": "1.0",
        }
        output = self.get_rendered_output(input_data)
        assert output == expected_output

    def test_render_scalar_input(self):
        input_data = "Just a test"
        expected_output = {"data": "Just a test", "apiVersion": "1.0"}
        output = self.get_rendered_output(input_data)
        assert output == expected_output
