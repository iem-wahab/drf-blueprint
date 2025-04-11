from django.urls import path

from drf_starter_template.examples.views import ErrorExampleApi
from drf_starter_template.examples.views import TodoCreateApi
from drf_starter_template.examples.views import TodoDeleteApi
from drf_starter_template.examples.views import TodoDetailApi
from drf_starter_template.examples.views import TodoHardDeleteApi
from drf_starter_template.examples.views import TodoListApi
from drf_starter_template.examples.views import TodoUpdateApi

app_name = "examples"


urlpatterns = [
    path("todos/", TodoListApi.as_view(), name="todo-list"),
    path("todos/create/", TodoCreateApi.as_view(), name="todo-create"),
    path("todos/<uuid:todo_id>/", TodoDetailApi.as_view(), name="todo-detail"),
    path("todos/<uuid:todo_id>/update/", TodoUpdateApi.as_view(), name="todo-update"),
    path("todos/<uuid:todo_id>/delete/", TodoDeleteApi.as_view(), name="todo-delete"),
    path(
        "todos/<uuid:todo_id>/hard-delete/",
        TodoHardDeleteApi.as_view(),
        name="todo-hard-delete",
    ),
    path("error-examples/", ErrorExampleApi.as_view(), name="error-examples"),
]
