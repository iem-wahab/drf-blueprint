from typing import Any

from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import exceptions
from rest_framework.authtoken.models import Token

from .models import User


@transaction.atomic
def user_create(*, email: str, password: str, name: str = "") -> User:
    user = User(email=email, name=name)
    user.set_password(password)
    user.full_clean()
    user.save()
    Token.objects.create(user=user)
    return user


@transaction.atomic
def user_update(*, user: User, data: dict[str, Any]) -> User:
    non_side_effect_fields = ["name", "email"]
    for field in non_side_effect_fields:
        if field in data:
            setattr(user, field, data[field])
    user.full_clean()
    user.save()
    return user


def validate_login_input(
    *, email: str, password: str, request: object | None = None
) -> User:
    user = authenticate(request=request, username=email, password=password)
    if not user:
        message = "Unable to log in with provided credentials."
        raise ValueError(message)
    return user


@transaction.atomic
def user_login(*, email: str, password: str, request: object | None = None) -> dict:
    try:
        user = validate_login_input(email=email, password=password, request=request)
    except ValueError as e:
        raise exceptions.ValidationError({"detail": str(e)}) from e

    token, _ = Token.objects.get_or_create(user=user)
    permissions = list(user.get_all_permissions())
    return {
        "token": token.key,
        "user_id": user.pk,
        "permissions": permissions,
    }
