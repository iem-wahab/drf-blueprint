from django.test import TestCase

from drf_starter_template.users.selectors import user_list
from drf_starter_template.users.tests.factories import UserFactory


class UserListTests(TestCase):
    def test_user_list_all(self):
        users = [UserFactory() for _ in range(3)]
        user_emails = {user.email for user in users}

        result = user_list()

        assert result.count() == 3
        for user in result:
            assert user.email in user_emails

    def test_user_list_with_empty_database(self):
        result = user_list()

        assert result.count() == 0

    def test_user_list_filter_by_id(self):
        users = [UserFactory() for _ in range(3)]
        user_to_find = users[1]

        result = user_list(filters={"id": user_to_find.id})

        assert result.count() == 1
        assert str(result.first().id) == str(user_to_find.id)

    def test_user_list_filter_by_email(self):
        UserFactory(email="user1@example.com")
        user_to_find = UserFactory(email="special@example.com")
        UserFactory(email="user3@example.com")

        result = user_list(filters={"email": "special@example.com"})

        assert result.count() == 1
        assert result.first().email == user_to_find.email

    def test_user_list_filter_by_name(self):
        UserFactory(name="John Doe")
        user_to_find = UserFactory(name="Jane Smith")
        UserFactory(name="Bob Johnson")

        result = user_list(filters={"name": "Jane Smith"})

        assert result.count() == 1
        assert result.first().name == user_to_find.name

    def test_user_list_filter_multiple_criteria(self):
        UserFactory(name="John Doe", email="john@example.com")
        user_to_find = UserFactory(name="Jane Smith", email="jane@example.com")
        UserFactory(name="Jane Johnson", email="janej@example.com")

        result = user_list(filters={"name": "Jane Smith", "email": "jane@example.com"})

        assert result.count() == 1
        assert result.first().name == user_to_find.name
        assert result.first().email == user_to_find.email

    def test_user_list_filter_no_match(self):
        UserFactory(name="John Doe")
        UserFactory(name="Jane Smith")

        result = user_list(filters={"name": "Nonexistent User"})

        assert result.count() == 0
