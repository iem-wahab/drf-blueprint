import uuid
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

EMAIL_REQUIRED = "The given email must be set"
SUPERUSER_STAFF_REQUIRED = "Superuser must have is_staff=True."
SUPERUSER_STATUS_REQUIRED = "Superuser must have is_superuser=True."


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(EMAIL_REQUIRED)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(SUPERUSER_STAFF_REQUIRED)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(SUPERUSER_STATUS_REQUIRED)

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None
    last_name = None
    email = models.EmailField(_("email address"), unique=True)
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        return reverse("users:user-detail", kwargs={"user_id": self.id})
