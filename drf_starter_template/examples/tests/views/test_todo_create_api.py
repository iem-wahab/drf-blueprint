import json
from typing import Any

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from drf_starter_template.examples.models import Todo
from drf_starter_template.examples.tests.factories import HighPriorityTodoFactory
from drf_starter_template.examples.tests.factories import LowPriorityTodoFactory
from drf_starter_template.examples.tests.factories import TodoFactory
from drf_starter_template.users.tests.factories import UserFactory


class TodoListCreateApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.user.has_perm = lambda perm: True
        examples_group, created = Group.objects.get_or_create(name="Examples")
        self.user.groups.add(examples_group)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("examples:todo-create")
        self.todos = [
            TodoFactory(),
            HighPriorityTodoFactory(),
            LowPriorityTodoFactory(),
        ]

    def test_create_todo(self):
        payload: dict[str, Any] = {
            "title": "New Test Todo",
            "description": "This is a test todo",
            "priority": Todo.PRIORITY_HIGH,
        }
        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "apiVersion" in data
        todo = Todo.objects.get(title="New Test Todo")
        assert todo.description == "This is a test todo"
        assert todo.priority == Todo.PRIORITY_HIGH
        assert not todo.completed

    def test_create_todo_with_invalid_data(self):
        payload: dict[str, Any] = {
            "title": "",
            "priority": "invalid-priority",
        }
        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "error" in data
        assert "extra" in data["error"]
        extra = data["error"]["extra"]
        detail = extra.get("detail")
        detail = str(extra).lower() if not detail else detail.lower()
        assert "title" in detail or "priority" in detail

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        response = self.client.post(
            self.url,
            data=json.dumps({"title": "Test"}),
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
