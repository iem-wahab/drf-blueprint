from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from drf_starter_template.users.tests.factories import UserFactory


class UserUpdateApiTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(email="old@example.com", name="Old Name")
        from drf_starter_template.users.models import User

        content_type = ContentType.objects.get_for_model(User)
        change_permission, _ = Permission.objects.get_or_create(
            codename="change_user",
            content_type=content_type,
            defaults={"name": "Can change user"},
        )
        group = Group.objects.create(name="ChangeGroupForTest")
        group.permissions.add(change_permission)
        self.user.groups.add(group)

        self.client.force_authenticate(user=self.user)
        self.url = reverse("users:user-update", kwargs={"user_id": self.user.id})

    def test_update_user_success(self):
        payload = {"email": "updated@example.com", "name": "Updated Name"}
        response = self.client.put(self.url, data=payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        data = response.json().get("data")
        assert data is not None
        assert data["email"] == payload["email"]
        assert data["name"] == payload["name"]

    def test_update_user_invalid_data(self):
        payload = {"email": "not-an-email"}
        response = self.client.put(self.url, data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
