from django.test import TestCase

from drf_starter_template.users.models import User
from drf_starter_template.users.selectors import UserFilter
from drf_starter_template.users.tests.factories import UserFactory


class UserFilterTests(TestCase):
    def test_filter_fields(self):
        filter_fields = UserFilter.Meta.fields

        assert "id" in filter_fields
        assert "email" in filter_fields
        assert "name" in filter_fields
        assert len(filter_fields) == 3

    def test_filter_by_id(self):
        users = [UserFactory() for _ in range(3)]
        user_to_find = users[0]

        filtered = UserFilter({"id": user_to_find.id}, queryset=User.objects.all()).qs

        assert filtered.count() == 1
        assert str(filtered.first().id) == str(user_to_find.id)

    def test_filter_by_email(self):
        UserFactory(email="user1@example.com")
        user_to_find = UserFactory(email="target@example.com")
        UserFactory(email="user3@example.com")

        filtered = UserFilter(
            {"email": "target@example.com"}, queryset=User.objects.all()
        ).qs

        assert filtered.count() == 1
        assert filtered.first().email == user_to_find.email

    def test_filter_by_name(self):
        UserFactory(name="John Doe")
        user_to_find = UserFactory(name="Target User")
        UserFactory(name="Jane Smith")

        filtered = UserFilter({"name": "Target User"}, queryset=User.objects.all()).qs

        assert filtered.count() == 1
        assert filtered.first().name == user_to_find.name

    def test_filter_by_multiple_fields(self):
        UserFactory(name="John Doe", email="john@example.com")
        user_to_find = UserFactory(name="Target User", email="target@example.com")
        UserFactory(name="Target User", email="wrong@example.com")

        filtered = UserFilter(
            {"name": "Target User", "email": "target@example.com"},
            queryset=User.objects.all(),
        ).qs

        assert filtered.count() == 1
        assert filtered.first().name == user_to_find.name
        assert filtered.first().email == user_to_find.email
