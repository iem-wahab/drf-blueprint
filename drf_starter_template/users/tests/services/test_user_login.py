import pytest
from django.test import TestCase
from rest_framework import exceptions
from rest_framework.authtoken.models import Token

from drf_starter_template.users.services import user_login
from drf_starter_template.users.tests.factories import UserFactory

TEST_PASSWORD = "testpassword123"  # noqa: S105
TEST_WRONG_PASSWORD = "wrongpassword"  # noqa: S105


class UserLoginTests(TestCase):
    def test_user_login_with_valid_credentials(self):
        user = UserFactory()
        password = TEST_PASSWORD
        user.set_password(password)
        user.save()

        token = Token.objects.create(user=user)

        login_data = user_login(email=user.email, password=password)

        assert login_data["token"] == token.key
        assert str(login_data["user_id"]) == str(user.pk)
        assert isinstance(login_data["permissions"], list)

    def test_user_login_creates_token_if_not_exists(self):
        user = UserFactory()
        password = TEST_PASSWORD
        user.set_password(password)
        user.save()

        Token.objects.filter(user=user).delete()

        login_data = user_login(email=user.email, password=password)

        token = Token.objects.get(user=user)

        assert login_data["token"] == token.key
        assert str(login_data["user_id"]) == str(user.pk)

    def test_user_login_with_invalid_credentials(self):
        user = UserFactory()
        password = TEST_PASSWORD
        user.set_password(password)
        user.save()

        with pytest.raises(exceptions.ValidationError):
            user_login(email=user.email, password=TEST_WRONG_PASSWORD)

    def test_user_login_with_request(self):
        user = UserFactory()
        password = TEST_PASSWORD
        user.set_password(password)
        user.save()

        class MockRequest:
            pass

        request = MockRequest()

        login_data = user_login(email=user.email, password=password, request=request)

        assert str(login_data["user_id"]) == str(user.pk)
