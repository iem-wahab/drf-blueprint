import uuid

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.test import TestCase

from drf_starter_template.users.selectors import user_get
from drf_starter_template.users.tests.factories import UserFactory


class UserGetTests(TestCase):
    def test_user_get_existing_user(self):
        user = UserFactory()

        retrieved_user = user_get(user_id=str(user.id))

        assert str(retrieved_user.id) == str(user.id)
        assert retrieved_user.email == user.email
        assert retrieved_user.name == user.name

    def test_user_get_nonexistent_user(self):
        non_existent_id = str(uuid.uuid4())

        with pytest.raises(ObjectDoesNotExist):
            user_get(user_id=non_existent_id)

    def test_user_get_with_invalid_id_format(self):
        invalid_id = "not-a-uuid"

        with pytest.raises(ValidationError):
            user_get(user_id=invalid_id)
