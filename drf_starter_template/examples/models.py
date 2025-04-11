from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from drf_starter_template.core.models import BaseModel


class Todo(BaseModel):
    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, _("Low")),
        (PRIORITY_MEDIUM, _("Medium")),
        (PRIORITY_HIGH, _("High")),
    ]

    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"), blank=True)
    completed = models.BooleanField(_("Completed"), default=False)
    priority = models.CharField(
        _("Priority"),
        max_length=20,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM,
    )
    due_date = models.DateField(_("Due Date"), null=True, blank=True)

    def clean(self):
        super().clean()

        if self.due_date:
            today = timezone.now().date()
            if self.due_date < today and not self.completed:
                raise ValidationError(
                    {
                        "due_date": _(
                            "Due date cannot be in the past for an incomplete Todo."
                        )
                    }
                )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Todo")
        verbose_name_plural = _("Todos")
        ordering = ["due_date", "priority"]
