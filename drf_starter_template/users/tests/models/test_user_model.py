import pytest
from django.test import TestCase
from django.urls import reverse

from drf_starter_template.users.models import User
from drf_starter_template.users.tests.factories import UserFactory

# Test password constant - S105 warning ignored as this is test code
TEST_PASSWORD = "testpass123"  # noqa: S105


class UserModelTests(TestCase):
    def test_user_str(self):
        user = UserFactory(email="test@example.com")
        assert str(user.email) == "test@example.com"

    def test_user_get_absolute_url(self):
        user = UserFactory()
        url = user.get_absolute_url()
        assert url == reverse("users:user-detail", kwargs={"user_id": user.id})

    def test_create_user_without_email_raises_error(self):
        with pytest.raises(ValueError, match="The given email must be set"):
            User.objects.create_user(email="", password=TEST_PASSWORD)

    def test_create_superuser_with_is_staff_false_raises_error(self):
        with pytest.raises(ValueError, match="Superuser must have is_staff=True"):
            User.objects.create_superuser(
                email="admin@example.com", password=TEST_PASSWORD, is_staff=False
            )

    def test_create_superuser_with_is_superuser_false_raises_error(self):
        with pytest.raises(ValueError, match="Superuser must have is_superuser=True"):
            User.objects.create_superuser(
                email="admin@example.com", password=TEST_PASSWORD, is_superuser=False
            )

    def test_create_user_normalizes_email(self):
        email = "Test@EXAMPLE.com"
        user = User.objects.create_user(email=email, password=TEST_PASSWORD)
        assert user.email == "Test@example.com"
