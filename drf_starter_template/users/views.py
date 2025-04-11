from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from drf_starter_template.core.views import BaseAPIView

from .models import User
from .selectors import user_list
from .services import user_create
from .services import user_login
from .services import user_update


class LoginApi(BaseAPIView):
    permission_classes = []

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField(label="Email")
        password = serializers.CharField(
            label="Password", style={"input_type": "password"}, trim_whitespace=False
        )

    class OutputSerializer(serializers.Serializer):
        token = serializers.CharField()
        user_id = serializers.UUIDField()
        permissions = serializers.ListField(child=serializers.CharField())

    @extend_schema(
        request=InputSerializer,
        responses=OutputSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        login_data = user_login(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            request=request,
        )

        return Response(login_data)


class UserListApi(BaseAPIView):
    models = [User]
    pagination_class = None

    class FilterSerializer(serializers.Serializer):
        id = serializers.UUIDField(required=False)
        email = serializers.EmailField(required=False)
        name = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        email = serializers.EmailField()
        name = serializers.CharField()

    @extend_schema(
        request=FilterSerializer,
        responses=OutputSerializer(many=True),
    )
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = user_list(filters=filters_serializer.validated_data)

        data = self.OutputSerializer(users, many=True).data
        return Response(data)


class UserCreateApi(BaseAPIView):
    models = [User]

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(min_length=8, write_only=True)
        name = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        email = serializers.EmailField()
        name = serializers.CharField()

    @extend_schema(
        request=InputSerializer,
        responses=OutputSerializer,
    )
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_create(**serializer.validated_data)

        response_serializer = self.OutputSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class UserDetailApi(BaseAPIView):
    models = [User]

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        email = serializers.EmailField()
        name = serializers.CharField()

    @extend_schema(
        request=None,
        responses=OutputSerializer,
    )
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = self.OutputSerializer(user)
        return Response(serializer.data)


class UserUpdateApi(BaseAPIView):
    models = [User]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        email = serializers.EmailField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        email = serializers.EmailField()
        name = serializers.CharField()

    @extend_schema(
        request=InputSerializer,
        responses=OutputSerializer,
    )
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_user = user_update(user=user, data=serializer.validated_data)

        response_serializer = self.OutputSerializer(updated_user)
        return Response(response_serializer.data)
