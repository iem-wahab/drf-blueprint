from typing import Any

import django_filters
from django.db.models import QuerySet

from .models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ("id", "email", "name")


def user_get(*, user_id: str) -> User:
    return User.objects.get(id=user_id)


def user_list(*, filters: dict[str, Any] | None = None) -> QuerySet[User]:
    filters = filters or {}
    qs = User.objects.all()

    return UserFilter(filters, qs).qs
