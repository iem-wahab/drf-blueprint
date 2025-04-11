from django.db.models.query import QuerySet
from rest_framework.generics import get_object_or_404

from drf_starter_template.examples.models import Todo


def todo_list(*, filters=None) -> QuerySet:
    filters = filters or {}
    qs = Todo.objects.filter(is_deleted=False)

    title = filters.get("title")
    if title:
        qs = qs.filter(title__icontains=title)

    priority = filters.get("priority")
    if priority:
        qs = qs.filter(priority=priority)

    completed = filters.get("completed")
    if completed is not None:
        qs = qs.filter(completed=completed)

    return qs


def todo_get(*, todo_id, include_deleted=False) -> Todo:
    queryset = Todo.objects
    if not include_deleted:
        queryset = queryset.filter(is_deleted=False)
    return get_object_or_404(queryset, id=todo_id)
