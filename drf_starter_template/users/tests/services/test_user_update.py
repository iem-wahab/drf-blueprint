import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from drf_starter_template.users.services import user_update
from drf_starter_template.users.tests.factories import UserFactory
from drf_starter_template.utils.faker import faker


class UserUpdateTests(TestCase):
    def test_user_update_name(self):
        user = UserFactory()
        original_email = user.email
        new_name = faker.name()

        updated_user = user_update(user=user, data={"name": new_name})

        assert updated_user.name == new_name
        assert updated_user.email == original_email

    def test_user_update_email(self):
        user = UserFactory()
        original_name = user.name
        new_email = faker.email()

        updated_user = user_update(user=user, data={"email": new_email})

        assert updated_user.email == new_email
        assert updated_user.name == original_name

    def test_user_update_multiple_fields(self):
        user = UserFactory()
        new_name = faker.name()
        new_email = faker.email()

        updated_user = user_update(
            user=user, data={"name": new_name, "email": new_email}
        )

        assert updated_user.name == new_name
        assert updated_user.email == new_email

    def test_user_update_with_invalid_email(self):
        user = UserFactory()
        invalid_email = "invalid-email"

        with pytest.raises(ValidationError):
            user_update(user=user, data={"email": invalid_email})

    def test_user_update_with_duplicate_email(self):
        user1 = UserFactory()
        user2 = UserFactory()

        with pytest.raises(ValidationError):
            user_update(user=user1, data={"email": user2.email})

    def test_user_update_with_empty_data(self):
        user = UserFactory()
        original_name = user.name
        original_email = user.email

        updated_user = user_update(user=user, data={})

        assert updated_user.name == original_name
        assert updated_user.email == original_email
