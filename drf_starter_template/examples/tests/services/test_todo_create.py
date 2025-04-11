import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from drf_starter_template.examples.models import Todo
from drf_starter_template.examples.services import todo_create
from drf_starter_template.utils.faker import faker


class TodoCreateTests(TestCase):
    def test_todo_create_with_valid_data(self):
        title = faker.sentence(nb_words=5)
        description = faker.paragraph()
        priority = Todo.PRIORITY_HIGH

        todo = todo_create(title=title, description=description, priority=priority)

        assert todo.title == title
        assert todo.description == description
        assert todo.priority == priority
        assert not todo.completed
        assert todo.due_date is None

    def test_todo_create_with_minimal_data(self):
        title = faker.sentence(nb_words=5)

        todo = todo_create(title=title)

        assert todo.title == title
        assert todo.description == ""
        assert todo.priority == Todo.PRIORITY_MEDIUM
        assert not todo.completed
        assert todo.due_date is None

    def test_todo_create_with_empty_title(self):
        with pytest.raises(ValidationError):
            todo_create(title="")

        assert Todo.objects.count() == 0

    def test_todo_create_with_invalid_priority(self):
        with pytest.raises(ValidationError):
            todo_create(title="Test Todo", priority="invalid_priority")

        assert Todo.objects.count() == 0
