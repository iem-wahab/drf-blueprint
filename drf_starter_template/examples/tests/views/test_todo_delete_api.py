import uuid

from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from drf_starter_template.examples.tests.factories import TodoFactory
from drf_starter_template.users.tests.factories import UserFactory


class TodoDeleteApiTests(APITestCase):
    def setUp(self):
        self.todo = TodoFactory()
        self.url = reverse("examples:todo-delete", kwargs={"todo_id": self.todo.id})
        self.user = UserFactory()
        self.user.has_perm = lambda perm: True
        examples_group, _ = Group.objects.get_or_create(name="Examples")
        self.user.groups.add(examples_group)
        self.client.force_authenticate(user=self.user)

    def test_delete_todo(self):
        todo_id = self.todo.id
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        detail_url = reverse("examples:todo-detail", kwargs={"todo_id": todo_id})
        response_detail = self.client.get(detail_url)
        assert response_detail.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_todo(self):
        nonexistent_url = reverse(
            "examples:todo-delete", kwargs={"todo_id": uuid.uuid4()}
        )
        response = self.client.delete(nonexistent_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "error" in data
        assert "message" in data["error"]

    def test_unauthenticated_access_delete(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_http_methods_not_allowed_on_delete(self):
        get_response = self.client.get(self.url)
        assert get_response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        put_response = self.client.put(
            self.url,
            content_type="application/json",
        )
        assert put_response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        post_response = self.client.post(self.url)
        assert post_response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_api_version_in_error_response_on_delete(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "apiVersion" in data
