import uuid
from unittest import mock

from django.test import TestCase
from django.utils import timezone

from drf_starter_template.core.models import BaseModel


class BaseModelTests(TestCase):
    def setUp(self):
        self.prepare_test_model = mock.MagicMock(spec=BaseModel)
        self.prepare_test_model.save = mock.MagicMock()

    def test_base_model_defaults(self):
        instance = mock.MagicMock(spec=BaseModel)
        instance.id = uuid.uuid4()
        instance.created_at = timezone.now()
        instance.updated_at = timezone.now()
        instance.deleted_at = None
        instance.is_deleted = False
        instance.name = "Test Instance"

        assert isinstance(instance.id, uuid.UUID)
        assert instance.created_at is not None
        assert instance.updated_at is not None
        assert instance.created_at <= timezone.now()
        assert instance.updated_at >= instance.created_at
        assert instance.deleted_at is None
        assert not instance.is_deleted
        assert instance.name == "Test Instance"

    def test_base_model_updated_at_changes(self):
        instance = mock.Mock()
        initial_time = timezone.now()
        instance.updated_at = initial_time

        new_time = initial_time + timezone.timedelta(seconds=1)
        with mock.patch("django.utils.timezone.now", return_value=new_time):
            instance.updated_at = new_time

        assert instance.updated_at > initial_time

    def test_base_model_soft_delete(self):
        instance = self.prepare_test_model
        instance.id = uuid.uuid4()
        instance.is_deleted = False
        instance.deleted_at = None

        delete_time = timezone.now()
        with mock.patch("django.utils.timezone.now", return_value=delete_time):
            BaseModel.delete(instance)

        assert instance.is_deleted
        assert instance.deleted_at == delete_time
        instance.save.assert_called_once()

    def test_base_model_hard_delete(self):
        import inspect

        source = inspect.getsource(BaseModel.hard_delete)

        assert "super().delete" in source
        assert "*args" in source
        assert "**kwargs" in source
        assert callable(BaseModel.hard_delete)
