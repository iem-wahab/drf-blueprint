from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from drf_starter_template.examples.models import Todo
from drf_starter_template.examples.tests.factories import CompletedTodoFactory
from drf_starter_template.examples.tests.factories import HighPriorityTodoFactory
from drf_starter_template.examples.tests.factories import LowPriorityTodoFactory
from drf_starter_template.examples.tests.factories import TodoFactory
from drf_starter_template.users.tests.factories import UserFactory


class TodoListApiTests(APITestCase):
    def setUp(self):
        self.url = reverse("examples:todo-list")
        self.user = UserFactory()
        self.user.has_perm = lambda perm: True
        examples_group, _ = Group.objects.get_or_create(name="Examples")
        self.user.groups.add(examples_group)
        self.client.force_authenticate(user=self.user)
        self.todo1 = TodoFactory(
            title="Todo1", priority=Todo.PRIORITY_LOW, completed=False
        )
        self.todo2 = HighPriorityTodoFactory(title="Todo2", completed=True)
        self.todo3 = LowPriorityTodoFactory(title="Todo3", completed=False)
        self.completed_todo = CompletedTodoFactory(title="Todo Completed")

    def test_list_all_todos(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "apiVersion" in data
        assert "data" in data
        titles = [todo["title"] for todo in data["data"]]
        assert "Todo1" in titles
        assert "Todo3" in titles
        assert "Todo2" not in titles
        assert "Todo Completed" not in titles

    def test_list_todos_with_priority_and_completed_filters(self):
        response = self.client.get(
            self.url, {"priority": Todo.PRIORITY_HIGH, "completed": True}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "data" in data
        assert len(data["data"]) == 1
        assert data["data"][0]["title"] == "Todo2"

    def test_list_todos_filter_by_completed(self):
        response = self.client.get(self.url, {"completed": True})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "data" in data
        completed_titles = [todo["title"] for todo in data["data"] if todo["completed"]]
        assert "Todo2" in completed_titles
        assert "Todo Completed" in completed_titles

    def test_list_todos_with_invalid_filter(self):
        response = self.client.get(self.url, {"priority": "invalid-priority"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "error" in data

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
