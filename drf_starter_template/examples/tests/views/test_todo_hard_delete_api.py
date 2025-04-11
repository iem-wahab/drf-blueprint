import uuid

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from drf_starter_template.examples.models import Todo
from drf_starter_template.examples.tests.factories import TodoFactory
from drf_starter_template.users.tests.factories import UserFactory


class TodoHardDeleteApiTests(APITestCase):
    def setUp(self):
        self.todo = TodoFactory()
        self.url = reverse(
            "examples:todo-hard-delete", kwargs={"todo_id": self.todo.id}
        )
        self.user = UserFactory()
        self.user.has_perm = lambda perm: True
        examples_group, created = Group.objects.get_or_create(name="Examples")
        self.user.groups.add(examples_group)
        self.client.force_authenticate(user=self.user)

    def test_hard_delete_todo(self):
        todo_id = self.todo.id
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Todo.objects.filter(id=todo_id).count() == 0

    def test_hard_delete_nonexistent_todo(self):
        nonexistent_url = reverse(
            "examples:todo-hard-delete", kwargs={"todo_id": uuid.uuid4()}
        )
        response = self.client.delete(nonexistent_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "error" in data
        assert "message" in data["error"]

    def test_hard_delete_already_soft_deleted_todo(self):
        self.todo.delete()
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_http_methods_not_allowed(self):
        get_response = self.client.get(self.url)
        assert get_response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        put_response = self.client.put(self.url)
        assert put_response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        post_response = self.client.post(self.url)
        assert post_response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_api_version_in_error_response(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        data = response.json()
        assert "apiVersion" in data
