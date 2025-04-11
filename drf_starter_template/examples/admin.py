from django.contrib import admin

from drf_starter_template.examples.models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "priority", "completed", "due_date", "created_at")
    list_filter = ("priority", "completed", "is_deleted")
    search_fields = ("title", "description")
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")
    fieldsets = (
        (None, {"fields": ("id", "title", "description")}),
        ("Status", {"fields": ("priority", "completed", "due_date")}),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at", "deleted_at", "is_deleted")},
        ),
    )
