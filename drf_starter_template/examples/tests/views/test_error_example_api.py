from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import override_settings

from drf_starter_template.users.tests.factories import UserFactory


@override_settings(API_DEFAULT_VERSION="1.0", DEBUG=False)
class ErrorHandlingTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.has_perm = lambda perm: True
        examples_group, _ = Group.objects.get_or_create(name="Examples")
        self.user.groups.add(examples_group)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("examples:error-examples")

    def test_not_found_error(self):
        response = self.client.get(f"{self.url}?error_type=not_found")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "apiVersion" in data
        assert "error" in data
        assert data["error"]["message"] == "That resource does not exist."
        assert data["error"]["code"] == 404

    def test_validation_error(self):
        response = self.client.get(f"{self.url}?error_type=validation")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        msg = data["error"]["message"]
        if isinstance(msg, list):
            msg = msg[0]
        assert "missing" in msg.lower() or "invalid" in msg.lower()
        assert data["error"]["code"] == 400

    def test_permission_error(self):
        response = self.client.get(f"{self.url}?error_type=permission")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        data = response.json()
        assert data["error"]["message"] == "You do not have permission to do that."
        assert data["error"]["code"] == 403

    def test_authentication_error(self):
        response = self.client.get(f"{self.url}?error_type=authentication")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        data = response.json()
        assert "apiVersion" in data
        assert "error" in data
        assert data["error"]["message"] == "You must be authenticated to do that."
        assert data["error"]["code"] == 403

    def test_throttling_error(self):
        response = self.client.get(f"{self.url}?error_type=throttling")
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        data = response.json()
        assert "apiVersion" in data
        assert "error" in data
        assert (
            data["error"]["message"]
            == "Request was throttled. Expected available in 60 seconds."
        )
        assert data["error"]["code"] == 429

    def test_server_error(self):
        response = self.client.get(f"{self.url}?error_type=server")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "apiVersion" in data
        assert "error" in data
        assert data["error"]["message"] == "Internal Server Error"
        assert data["error"]["code"] == 500
        assert data["error"]["extra"] == {"detail": "Unhandled exception occurred"}

    def test_application_error(self):
        response = self.client.get(f"{self.url}?error_type=application")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        data = response.json()
        assert "apiVersion" in data
        assert "error" in data
        assert data["error"]["message"] == "Unexpected error occurred on the server."
        assert data["error"]["code"] == 500

    def test_default_response(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "apiVersion" in data
        assert "data" in data
        assert (
            data["data"]["message"] == "No error specified. Use ?error_type parameter."
        )
