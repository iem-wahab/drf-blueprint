from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from drf_starter_template.users.models import User
from drf_starter_template.users.tests.factories import UserFactory


class UserListApiTests(APITestCase):
    def setUp(self):
        self.users = [UserFactory() for _ in range(3)]
        self.user = UserFactory()
        content_type = ContentType.objects.get_for_model(User)
        view_permission, _ = Permission.objects.get_or_create(
            codename="view_user",
            content_type=content_type,
            defaults={"name": "Can view user"},
        )
        group = Group.objects.create(name="ViewGroupForTest")
        group.permissions.add(view_permission)
        self.user.groups.add(group)

        self.client.force_authenticate(user=self.user)
        self.url = reverse("users:user-list")

    def test_user_list_returns_all_users(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json().get("data")
        assert data is not None
        assert len(data) == User.objects.count()

        for user_data in data:
            assert "id" in user_data
            assert "email" in user_data
            assert "name" in user_data

    def test_user_list_filter_by_email(self):
        UserFactory(email="target@example.com")
        response = self.client.get(self.url, {"email": "target@example.com"})
        assert response.status_code == status.HTTP_200_OK
        data = response.json().get("data")
        assert data is not None
        assert len(data) == 1
        assert data[0]["email"] == "target@example.com"
