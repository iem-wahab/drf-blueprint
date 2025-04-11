import uuid
from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from drf_starter_template.examples.models import Todo
from drf_starter_template.examples.tests.factories import TodoFactory


class TodoModelTests(TestCase):
    def setUp(self):
        self.todo = TodoFactory()

    def test_str_representation(self):
        assert str(self.todo) == self.todo.title

    def test_default_values(self):
        todo = Todo.objects.create(title="Test Default Values")
        assert todo.description == ""
        assert todo.priority == Todo.PRIORITY_MEDIUM
        assert not todo.completed
        assert todo.due_date is None
        assert todo.id is not None
        assert not todo.is_deleted
        assert todo.deleted_at is None

    def test_clean_method_with_completed_empty_title(self):
        todo = Todo(title="", completed=True)
        with pytest.raises(ValidationError) as excinfo:
            todo.full_clean()

        errors = excinfo.value.message_dict
        assert "title" in errors

    def test_model_fields(self):
        title = "Test Todo"
        description = "This is a test description"
        priority = Todo.PRIORITY_HIGH
        due_date = timezone.now().date() + timedelta(days=5)

        todo = Todo.objects.create(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            completed=True,
        )

        saved_todo = Todo.objects.get(id=todo.id)

        assert saved_todo.title == title
        assert saved_todo.description == description
        assert saved_todo.priority == priority
        assert saved_todo.due_date == due_date
        assert saved_todo.completed

    def test_soft_delete(self):
        todo = TodoFactory()
        original_count = Todo.objects.count()

        todo.delete()

        assert Todo.objects.count() == original_count
        updated_todo = Todo.objects.get(id=todo.id)
        assert updated_todo.is_deleted
        assert updated_todo.deleted_at is not None

        assert Todo.objects.filter(is_deleted=False).count() == original_count - 1

    def test_hard_delete(self):
        todo = TodoFactory()
        original_count = Todo.objects.count()

        todo.hard_delete()

        assert Todo.objects.count() == original_count - 1
        with pytest.raises(Todo.DoesNotExist):
            Todo.objects.get(id=todo.id)

    def test_uuid_generation(self):
        todo = Todo.objects.create(title="UUID Test")
        assert isinstance(todo.id, uuid.UUID)
        assert bool(todo.id)
