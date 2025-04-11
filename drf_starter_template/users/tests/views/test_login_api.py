from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from drf_starter_template.users.models import User
from drf_starter_template.users.tests.factories import UserFactory


class LoginApiViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("api-login")
        self.user = UserFactory(email="test@example.com")
        self.user.set_password("testpassword123")
        self.user.save()

        self.content_type = ContentType.objects.get_for_model(User)
        self.permission = Permission.objects.create(
            codename="test_permission",
            name="Test permission",
            content_type=self.content_type,
        )

        self.group = Group.objects.create(name="TestGroup")
        self.group.permissions.add(self.permission)
        self.user.groups.add(self.group)

    def test_login_successful(self):
        data = {"email": "test@example.com", "password": "testpassword123"}

        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_200_OK

        response_json = response.json()
        assert "apiVersion" in response_json
        assert "data" in response_json

        response_data = response_json["data"]
        assert "token" in response_data
        assert "userId" in response_data
        assert "permissions" in response_data

        assert response_data["token"]

        assert str(self.user.id) == response_data["userId"]

        expected_permission = (
            f"{self.content_type.app_label}.{self.permission.codename}"
        )
        assert expected_permission in response_data["permissions"]

    def test_login_invalid_credentials(self):
        data = {"email": "test@example.com", "password": "wrongpassword"}

        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_missing_fields(self):
        response = self.client.post(
            self.url, {"email": "test@example.com"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = self.client.post(
            self.url, {"password": "testpassword123"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = self.client.post(self.url, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_inactive_user(self):
        inactive_user = UserFactory(email="inactive@example.com", is_active=False)
        inactive_user.set_password("testpassword123")
        inactive_user.save()

        data = {"email": "inactive@example.com", "password": "testpassword123"}

        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_api_version_in_response(self):
        data = {"email": "test@example.com", "password": "testpassword123"}

        response = self.client.post(self.url, data, format="json")

        assert response.status_code == status.HTTP_200_OK

        response_json = response.json()
        assert "apiVersion" in response_json
        assert "data" in response_json
