from django.urls import path

from .views import UserCreateApi
from .views import UserDetailApi
from .views import UserListApi
from .views import UserUpdateApi

app_name = "users"

urlpatterns = [
    path("", UserListApi.as_view(), name="user-list"),
    path("<uuid:user_id>/", UserDetailApi.as_view(), name="user-detail"),
    path("create/", UserCreateApi.as_view(), name="user-create"),
    path("<uuid:user_id>/update/", UserUpdateApi.as_view(), name="user-update"),
]
