import uuid

import pytest
from django.http import Http404
from django.test import TestCase

from drf_starter_template.examples.models import Todo
from drf_starter_template.examples.selectors import todo_get
from drf_starter_template.examples.selectors import todo_list
from drf_starter_template.examples.tests.factories import CompletedTodoFactory
from drf_starter_template.examples.tests.factories import HighPriorityTodoFactory
from drf_starter_template.examples.tests.factories import LowPriorityTodoFactory
from drf_starter_template.examples.tests.factories import TodoFactory


class TodoSelectorsTests(TestCase):
    def setUp(self):
        self.medium_priority_todo = TodoFactory(
            title="Medium Priority Task",
            description="This is a medium priority task",
            completed=False,
        )

        self.high_priority_todo = HighPriorityTodoFactory(
            title="High Priority Task",
            description="This is a high priority task",
            completed=False,
        )

        self.low_priority_todo = LowPriorityTodoFactory(
            title="Low Priority Task",
            description="This is a low priority task",
            completed=False,
        )

        self.completed_todo = CompletedTodoFactory(
            title="Completed Task",
            description="This is a completed task",
        )

        self.deleted_todo = TodoFactory(title="Deleted Task")
        self.deleted_todo.delete()

    def test_todo_list_no_filters(self):
        todos = todo_list(filters={})
        assert todos.count() == 4
        assert self.medium_priority_todo in todos
        assert self.high_priority_todo in todos
        assert self.low_priority_todo in todos
        assert self.completed_todo in todos
        assert self.deleted_todo not in todos

    def test_todo_list_filter_by_title(self):
        todos = todo_list(filters={"title": "High Priority Task"})
        assert todos.count() == 1
        assert self.high_priority_todo in todos

        todos = todo_list(filters={"title": "priority"})
        assert todos.count() == 3
        assert self.medium_priority_todo in todos
        assert self.high_priority_todo in todos
        assert self.low_priority_todo in todos

        todos = todo_list(filters={"title": "non-existent"})
        assert todos.count() == 0

    def test_todo_list_filter_by_priority(self):
        todos = todo_list(filters={"priority": Todo.PRIORITY_HIGH})
        assert todos.count() == 1
        assert self.high_priority_todo in todos

        todos = todo_list(filters={"priority": Todo.PRIORITY_MEDIUM})
        assert todos.count() == 2

        todos = todo_list(filters={"priority": Todo.PRIORITY_LOW})
        assert todos.count() == 1
        assert self.low_priority_todo in todos

    def test_todo_list_filter_by_completed(self):
        todos = todo_list(filters={"completed": True})
        assert todos.count() == 1
        assert self.completed_todo in todos

        todos = todo_list(filters={"completed": False})
        assert todos.count() == 3
        assert self.medium_priority_todo in todos
        assert self.high_priority_todo in todos
        assert self.low_priority_todo in todos

    def test_todo_list_combined_filters(self):
        additional_todo = TodoFactory(
            title="Medium Priority Completed",
            priority=Todo.PRIORITY_MEDIUM,
            completed=True,
        )

        todos = todo_list(filters={"priority": Todo.PRIORITY_MEDIUM, "completed": True})
        expected_count = Todo.objects.filter(
            is_deleted=False, priority=Todo.PRIORITY_MEDIUM, completed=True
        ).count()
        assert todos.count() == expected_count
        assert additional_todo in todos

        todos = todo_list(filters={"title": "priority", "priority": Todo.PRIORITY_HIGH})
        assert todos.count() == 1
        assert self.high_priority_todo in todos

    def test_todo_get_with_valid_id(self):
        todo = todo_get(todo_id=self.medium_priority_todo.id)
        assert todo == self.medium_priority_todo

    def test_todo_get_with_invalid_id(self):
        non_existent_id = uuid.uuid4()
        with pytest.raises(Http404):
            todo_get(todo_id=non_existent_id)

    def test_todo_get_with_deleted_todo(self):
        with pytest.raises(Http404):
            todo_get(todo_id=self.deleted_todo.id)
