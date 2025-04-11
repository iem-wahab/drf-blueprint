import pytest
from django.test import TestCase

from drf_starter_template.users.services import validate_login_input
from drf_starter_template.users.tests.factories import UserFactory

TEST_PASSWORD = "testpassword123"  # noqa: S105
TEST_WRONG_PASSWORD = "wrongpassword"  # noqa: S105
ERROR_MESSAGE = "Unable to log in with provided credentials."


class ValidateLoginInputTests(TestCase):
    def test_validate_login_input_with_valid_credentials(self):
        user = UserFactory()
        password = TEST_PASSWORD
        user.set_password(password)
        user.save()

        authenticated_user = validate_login_input(email=user.email, password=password)

        assert str(authenticated_user.pk) == str(user.pk)

    def test_validate_login_input_with_invalid_email(self):
        user = UserFactory()
        password = TEST_PASSWORD
        user.set_password(password)
        user.save()

        with pytest.raises(ValueError, match=ERROR_MESSAGE):
            validate_login_input(email="wrong-email@example.com", password=password)

    def test_validate_login_input_with_invalid_password(self):
        user = UserFactory()
        password = TEST_PASSWORD
        user.set_password(password)
        user.save()

        with pytest.raises(ValueError, match=ERROR_MESSAGE):
            validate_login_input(email=user.email, password=TEST_WRONG_PASSWORD)

    def test_validate_login_input_with_request(self):
        user = UserFactory()
        password = TEST_PASSWORD
        user.set_password(password)
        user.save()

        class MockRequest:
            pass

        request = MockRequest()

        authenticated_user = validate_login_input(
            email=user.email, password=password, request=request
        )

        assert str(authenticated_user.pk) == str(user.pk)
