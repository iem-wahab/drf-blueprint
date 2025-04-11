import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.authtoken.models import Token

from drf_starter_template.users.models import User
from drf_starter_template.users.services import user_create
from drf_starter_template.utils.faker import faker

TEST_PASSWORD = "testpassword123"  # noqa: S105


class UserCreateTests(TestCase):
    def test_user_create_with_valid_data(self):
        email = faker.email()
        password = TEST_PASSWORD
        name = faker.name()

        user = user_create(email=email, password=password, name=name)

        assert user.email == email
        assert user.name == name
        assert user.check_password(password)

        assert Token.objects.filter(user=user).exists()

    def test_user_create_without_name(self):
        email = faker.email()
        password = TEST_PASSWORD

        user = user_create(email=email, password=password)

        assert user.email == email
        assert user.name == ""
        assert user.check_password(password)

        assert Token.objects.filter(user=user).exists()

    def test_user_create_with_invalid_email(self):
        email = "invalid-email"
        password = TEST_PASSWORD

        with pytest.raises(ValidationError):
            user_create(email=email, password=password)

        assert User.objects.count() == 0

    def test_user_create_with_duplicate_email(self):
        email = faker.email()
        password = TEST_PASSWORD

        user_create(email=email, password=password)

        with pytest.raises(ValidationError):
            user_create(email=email, password=password)

        assert User.objects.count() == 1
