from django.core.exceptions import ValidationError
from django.db import DataError
from django.db import IntegrityError

from drf_starter_template.examples.models import Todo


def todo_create(*, title, description=None, priority=None, due_date=None) -> Todo:
    todo = Todo(
        title=title,
        description=description or "",
        priority=priority or Todo.PRIORITY_MEDIUM,
        due_date=due_date,
    )
    try:
        todo.full_clean()
        todo.save()
    except (ValidationError, IntegrityError, DataError) as e:
        error_message = f"Failed to create todo: {e}"
        raise ValidationError(error_message) from e
    else:
        return todo


def todo_update(*, todo, data) -> Todo:
    for field, value in data.items():
        setattr(todo, field, value)
    try:
        todo.full_clean()
        todo.save()
    except (ValidationError, IntegrityError, DataError) as e:
        error_message = f"Failed to update todo: {e}"
        raise ValidationError(error_message) from e
    else:
        return todo


def todo_delete(*, todo) -> None:
    todo.delete()


def todo_hard_delete(*, todo) -> None:
    todo.hard_delete()
