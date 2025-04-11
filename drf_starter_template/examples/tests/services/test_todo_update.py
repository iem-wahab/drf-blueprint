import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from drf_starter_template.examples.models import Todo
from drf_starter_template.examples.services import todo_update
from drf_starter_template.examples.tests.factories import TodoFactory
from drf_starter_template.utils.faker import faker


class TodoUpdateTests(TestCase):
    def setUp(self):
        self.todo = TodoFactory()

    def test_todo_update_with_valid_data(self):
        new_title = faker.sentence(nb_words=5)
        new_description = faker.paragraph()
        new_priority = Todo.PRIORITY_HIGH
        new_completed = True

        data = {
            "title": new_title,
            "description": new_description,
            "priority": new_priority,
            "completed": new_completed,
        }

        updated_todo = todo_update(todo=self.todo, data=data)

        assert updated_todo.title == new_title
        assert updated_todo.description == new_description
        assert updated_todo.priority == new_priority
        assert updated_todo.completed == new_completed

    def test_todo_update_with_partial_data(self):
        original_title = self.todo.title
        new_description = faker.paragraph()

        data = {"description": new_description}

        updated_todo = todo_update(todo=self.todo, data=data)

        assert updated_todo.title == original_title
        assert updated_todo.description == new_description
        assert updated_todo.priority == self.todo.priority
        assert updated_todo.completed == self.todo.completed

    def test_todo_update_with_invalid_priority(self):
        original_priority = self.todo.priority
        data = {"priority": "invalid_priority"}
        todo_id = self.todo.id

        with pytest.raises(ValidationError):
            todo_update(todo=self.todo, data=data)

        reloaded_todo = Todo.objects.get(id=todo_id)
        assert reloaded_todo.priority == original_priority

    def test_todo_update_with_due_date(self):
        new_due_date = (timezone.now() + timezone.timedelta(days=10)).date()
        data = {"due_date": new_due_date}

        updated_todo = todo_update(todo=self.todo, data=data)
        assert updated_todo.due_date == new_due_date
