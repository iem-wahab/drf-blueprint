from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import Throttled
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from drf_starter_template.core.views import BaseAPIView
from drf_starter_template.examples.models import Todo
from drf_starter_template.examples.selectors import todo_get
from drf_starter_template.examples.selectors import todo_list
from drf_starter_template.examples.services import todo_create
from drf_starter_template.examples.services import todo_delete
from drf_starter_template.examples.services import todo_hard_delete
from drf_starter_template.examples.services import todo_update


class TodoListApi(BaseAPIView, ListAPIView):
    models = [Todo]

    class FilterSerializer(serializers.Serializer):
        title = serializers.CharField(required=False)
        priority = serializers.ChoiceField(
            choices=Todo.PRIORITY_CHOICES, required=False
        )
        completed = serializers.BooleanField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        completed = serializers.BooleanField()
        priority = serializers.ChoiceField(choices=Todo.PRIORITY_CHOICES)
        due_date = serializers.DateField(allow_null=True)
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

    @extend_schema(
        request=FilterSerializer,
        responses=OutputSerializer(many=True),
    )
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        todos = todo_list(filters=filters_serializer.validated_data)

        page = self.paginate_queryset(todos)
        if page is not None:
            serializer = self.OutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.OutputSerializer(todos, many=True)
        return Response(serializer.data)


class TodoCreateApi(BaseAPIView):
    models = [Todo]

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255)
        description = serializers.CharField(required=False, allow_blank=True)
        priority = serializers.ChoiceField(
            choices=Todo.PRIORITY_CHOICES, required=False
        )
        due_date = serializers.DateField(required=False, allow_null=True)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        completed = serializers.BooleanField()
        priority = serializers.ChoiceField(choices=Todo.PRIORITY_CHOICES)
        due_date = serializers.DateField(allow_null=True)
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

    @extend_schema(
        request=InputSerializer,
        responses=OutputSerializer,
    )
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        todo = todo_create(**serializer.validated_data)
        response_serializer = self.OutputSerializer(todo)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class TodoDetailApi(BaseAPIView):
    models = [Todo]

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        completed = serializers.BooleanField()
        priority = serializers.ChoiceField(choices=Todo.PRIORITY_CHOICES)
        due_date = serializers.DateField(allow_null=True)
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

    @extend_schema(
        request=None,
        responses=OutputSerializer,
    )
    def get(self, request, todo_id):
        todo = todo_get(todo_id=todo_id)
        serializer = self.OutputSerializer(todo)
        return Response(serializer.data)


class TodoUpdateApi(BaseAPIView):
    models = [Todo]

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=255, required=False)
        description = serializers.CharField(required=False, allow_blank=True)
        priority = serializers.ChoiceField(
            choices=Todo.PRIORITY_CHOICES, required=False
        )
        completed = serializers.BooleanField(required=False)
        due_date = serializers.DateField(required=False, allow_null=True)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        completed = serializers.BooleanField()
        priority = serializers.ChoiceField(choices=Todo.PRIORITY_CHOICES)
        due_date = serializers.DateField(allow_null=True)
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

    @extend_schema(
        request=InputSerializer,
        responses=OutputSerializer,
    )
    def put(self, request, todo_id):
        todo = todo_get(todo_id=todo_id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_todo = todo_update(todo=todo, data=serializer.validated_data)
        response_serializer = self.OutputSerializer(updated_todo)
        return Response(response_serializer.data)


class TodoDeleteApi(BaseAPIView):
    models = [Todo]

    @extend_schema(
        request=None,
        responses=None,
    )
    def delete(self, request, todo_id):
        todo = todo_get(todo_id=todo_id)
        todo_delete(todo=todo)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TodoHardDeleteApi(BaseAPIView):
    models = [Todo]

    @extend_schema(
        request=None,
        responses=None,
    )
    def delete(self, request, todo_id):
        todo = todo_get(todo_id=todo_id, include_deleted=True)
        todo_hard_delete(todo=todo)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ErrorExampleApi(BaseAPIView):
    models = [Todo]

    class InputSerializer(serializers.Serializer):
        error_type = serializers.ChoiceField(
            choices=[
                "not_found",
                "validation",
                "permission",
                "authentication",
                "throttling",
                "server",
                "application",
                "",
            ],
            required=False,
            default="",
        )

    class OutputSerializer(serializers.Serializer):
        message = serializers.CharField()

    @extend_schema(
        parameters=[InputSerializer],
        responses=OutputSerializer,
    )
    def get(self, request):
        serializer = self.InputSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        error_type = serializer.validated_data.get("error_type", "")

        if error_type == "not_found":
            error_message = "That resource does not exist."
            raise NotFound(error_message)
        if error_type == "validation":
            error_message = "Query param 'param' is missing."
            raise ValidationError(error_message)
        if error_type == "permission":
            error_message = "You do not have permission to do that."
            raise PermissionDenied(error_message)
        if error_type == "authentication":
            error_message = "You must be authenticated to do that."
            raise PermissionDenied(error_message)
        if error_type == "throttling":
            raise Throttled(60)
        if error_type == "server":
            error_message = "Division by zero"
            raise ZeroDivisionError(error_message)
        if error_type == "application":
            error_message = "Unexpected error occurred on the server."
            raise APIException(error_message)

        response_data = {"message": _("No error specified. Use ?error_type parameter.")}
        return Response(response_data)
