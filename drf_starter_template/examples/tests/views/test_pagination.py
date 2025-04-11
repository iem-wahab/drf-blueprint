from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from drf_starter_template.examples.tests.factories import TodoFactory
from drf_starter_template.users.tests.factories import UserFactory


class PaginationTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.has_perm = lambda perm: True
        examples_group, created = Group.objects.get_or_create(name="Examples")
        self.user.groups.add(examples_group)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("examples:todo-list")
        self.todos = [TodoFactory() for _ in range(25)]

    def test_default_pagination(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["meta"]["totalItems"] == 25
        assert data["meta"]["currentPage"] == 1
        assert data["meta"]["pageSize"] == 10
        assert data["meta"]["totalPages"] == 3
        assert len(data["data"]) == 10
        assert "links" in data
        assert "self" in data["links"]
        assert "first" in data["links"]
        assert "last" in data["links"]
        assert "next" in data["links"]
        assert data["links"]["previous"] is None
        assert data["links"]["next"] is not None

    def test_custom_page_size(self):
        response = self.client.get(f"{self.url}?page_size=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["meta"]["totalItems"] == 25
        assert data["meta"]["pageSize"] == 5
        assert data["meta"]["totalPages"] == 5
        assert len(data["data"]) == 5

    def test_page_navigation(self):
        response1 = self.client.get(f"{self.url}?page=1&page_size=5")
        data1 = response1.json()
        response2 = self.client.get(f"{self.url}?page=2&page_size=5")
        data2 = response2.json()
        response_last = self.client.get(f"{self.url}?page=5&page_size=5")
        data_last = response_last.json()
        first_page_ids = [item["id"] for item in data1["data"]]
        second_page_ids = [item["id"] for item in data2["data"]]
        assert len(set(first_page_ids).intersection(second_page_ids)) == 0
        assert data1["meta"]["currentPage"] == 1
        assert data2["meta"]["currentPage"] == 2
        assert data_last["meta"]["currentPage"] == 5
        assert data1["links"]["previous"] is None
        assert data1["links"]["next"] is not None
        assert data2["links"]["previous"] is not None
        assert data2["links"]["next"] is not None
        assert data_last["links"]["previous"] is not None
        assert data_last["links"]["next"] is None

    def test_invalid_page(self):
        response = self.client.get(f"{self.url}?page=999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "error" in data
        assert "message" in data["error"]

    def test_max_page_size(self):
        response = self.client.get(f"{self.url}?page_size=1000")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["meta"]["pageSize"] == 100

    def test_page_zero_or_negative(self):
        response_zero = self.client.get(f"{self.url}?page=0")
        data_zero = response_zero.json()
        response_negative = self.client.get(f"{self.url}?page=-1")
        data_negative = response_negative.json()
        assert data_zero["meta"]["currentPage"] == 1
        assert data_negative["meta"]["currentPage"] == 1
