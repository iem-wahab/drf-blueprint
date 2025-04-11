import uuid

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from drf_starter_template.users.models import User
from drf_starter_template.users.tests.factories import UserFactory


class UserDetailApiTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        content_type = ContentType.objects.get_for_model(User)
        view_permission, _ = Permission.objects.get_or_create(
            codename="view_user",
            content_type=content_type,
            defaults={"name": "Can view user"},
        )
        group = Group.objects.create(name="ViewGroupForDetailTest")
        group.permissions.add(view_permission)
        self.user.groups.add(group)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("users:user-detail", kwargs={"user_id": self.user.id})

    def test_get_user_detail_success(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json().get("data")
        assert data is not None
        assert data["id"] == str(self.user.id)
        assert data["email"] == self.user.email
        assert data["name"] == self.user.name

    def test_get_user_detail_not_found(self):
        non_existent_id = uuid.uuid4()
        url = reverse("users:user-detail", kwargs={"user_id": non_existent_id})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
