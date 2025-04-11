import json
import uuid

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from drf_starter_template.examples.tests.factories import TodoFactory
from drf_starter_template.users.tests.factories import UserFactory


class TodoDetailApiTests(APITestCase):
    def setUp(self):
        self.todo = TodoFactory()
        self.url = reverse("examples:todo-detail", kwargs={"todo_id": self.todo.id})
        self.user = UserFactory()
        self.user.has_perm = lambda perm: True
        examples_group, created = Group.objects.get_or_create(name="Examples")
        self.user.groups.add(examples_group)
        self.client.force_authenticate(user=self.user)

    def test_get_todo(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "apiVersion" in data
        assert "data" in data
        assert data["data"]["id"] == str(self.todo.id)
        assert data["data"]["title"] == self.todo.title
        assert data["data"]["description"] == self.todo.description
        assert data["data"]["priority"] == self.todo.priority
        assert data["data"]["completed"] == self.todo.completed

    def test_get_nonexistent_todo(self):
        nonexistent_url = reverse(
            "examples:todo-detail", kwargs={"todo_id": uuid.uuid4()}
        )
        response = self.client.get(nonexistent_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "error" in data
        assert "message" in data["error"]

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        get_response = self.client.get(self.url)
        assert get_response.status_code == status.HTTP_401_UNAUTHORIZED
        put_response = self.client.put(
            self.url,
            data=json.dumps({"title": "New title"}),
            content_type="application/json",
        )
        assert put_response.status_code == status.HTTP_401_UNAUTHORIZED
        delete_response = self.client.delete(self.url)
        assert delete_response.status_code == status.HTTP_401_UNAUTHORIZED
