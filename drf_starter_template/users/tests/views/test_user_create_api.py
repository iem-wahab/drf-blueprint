from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from drf_starter_template.users.tests.factories import UserFactory


class UserCreateApiTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        content_type = ContentType.objects.get_for_model(self.user.__class__)
        add_permission, _ = Permission.objects.get_or_create(
            codename="add_user",
            content_type=content_type,
            defaults={"name": "Can add user"},
        )
        group = Group.objects.create(name="AddGroupForTest")
        group.permissions.add(add_permission)
        self.user.groups.add(group)

        self.client.force_authenticate(user=self.user)
        self.url = reverse("users:user-create")

    def test_create_user_success(self):
        payload = {
            "email": "newuser@example.com",
            "password": "StrongPass123!",
            "name": "New User",
        }
        response = self.client.post(self.url, data=payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json().get("data")
        assert data is not None
        assert "id" in data
        assert data["email"] == payload["email"]
        assert data["name"] == payload.get("name", "")

    def test_create_user_invalid_data(self):
        payload = {"email": "", "password": "short"}
        response = self.client.post(self.url, data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
