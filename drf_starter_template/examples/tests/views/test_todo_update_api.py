import json
import uuid

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from drf_starter_template.examples.tests.factories import TodoFactory
from drf_starter_template.users.tests.factories import UserFactory


class TodoUpdateApiTests(APITestCase):
    def setUp(self):
        self.todo = TodoFactory()
        self.url = reverse("examples:todo-update", kwargs={"todo_id": self.todo.id})
        self.user = UserFactory()
        self.user.has_perm = lambda perm: True
        examples_group, _ = Group.objects.get_or_create(name="Examples")
        self.user.groups.add(examples_group)
        self.client.force_authenticate(user=self.user)

    def test_update_todo(self):
        payload = {
            "title": "Updated Todo",
            "description": "Updated description",
            "priority": self.todo.PRIORITY_LOW,
            "completed": True,
        }
        response = self.client.put(
            self.url,
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "apiVersion" in data
        assert "data" in data
        updated_todo = data["data"]
        assert updated_todo["title"] == payload["title"]
        assert updated_todo["description"] == payload["description"]
        assert updated_todo["priority"] == payload["priority"]
        assert updated_todo["completed"] == payload["completed"]

    def test_update_todo_invalid_data(self):
        payload = {
            "title": "",
            "priority": "invalid-priority",
        }
        response = self.client.put(
            self.url,
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "error" in data
        extra = data["error"].get("extra", {})
        assert ("title" in extra or "priority" in extra) or (
            "title" in str(extra).lower() or "priority" in str(extra).lower()
        )

    def test_update_nonexistent_todo(self):
        nonexistent_url = reverse(
            "examples:todo-update", kwargs={"todo_id": uuid.uuid4()}
        )
        response = self.client.put(
            nonexistent_url,
            data=json.dumps({"title": "Should not exist"}),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "error" in data
        assert "message" in data["error"]

    def test_unauthenticated_access_update(self):
        self.client.force_authenticate(user=None)
        response = self.client.put(
            self.url,
            data=json.dumps({"title": "Should not update"}),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
