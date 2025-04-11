from django.test import TestCase

from drf_starter_template.examples.models import Todo
from drf_starter_template.examples.services import todo_delete
from drf_starter_template.examples.services import todo_hard_delete
from drf_starter_template.examples.tests.factories import TodoFactory


class TodoDeleteTests(TestCase):
    def setUp(self):
        self.todo = TodoFactory()

    def test_todo_delete(self):
        todo_id = self.todo.id

        assert not self.todo.is_deleted
        assert self.todo.deleted_at is None

        todo_delete(todo=self.todo)

        updated_todo = Todo.objects.get(id=todo_id)
        assert updated_todo.is_deleted
        assert updated_todo.deleted_at is not None

        assert Todo.objects.filter(is_deleted=False).count() == 0

    def test_todo_hard_delete(self):
        todo_id = self.todo.id

        todo_hard_delete(todo=self.todo)

        assert Todo.objects.count() == 0
        assert Todo.objects.filter(id=todo_id).count() == 0

    def test_delete_multiple_todos(self):
        todo2 = TodoFactory()
        todo3 = TodoFactory()

        assert Todo.objects.count() == 3

        todo_delete(todo=self.todo)
        assert Todo.objects.count() == 3
        assert Todo.objects.filter(is_deleted=False).count() == 2

        todo_delete(todo=todo2)
        assert Todo.objects.count() == 3
        assert Todo.objects.filter(is_deleted=False).count() == 1

        todo_hard_delete(todo=todo3)
        assert Todo.objects.count() == 2
        assert Todo.objects.filter(is_deleted=False).count() == 0
