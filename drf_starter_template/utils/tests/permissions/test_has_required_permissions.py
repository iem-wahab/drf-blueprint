from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from drf_starter_template.users.models import User
from drf_starter_template.users.tests.factories import UserFactory
from drf_starter_template.utils.permissions import AdvancedDRFPermission


class MockUserView:
    models = [User]


class MockNoModelView:
    pass


class MockCustomPermissionsView:
    models = [User]
    has_all_permissions = ["{app}.view_user", "{app}.add_user"]
    has_any_permission = ["{app}.change_user", "{app}.delete_user"]

    def __init__(self):
        app_label = User._meta.app_label  # noqa: SLF001
        self.has_all_permissions = [
            perm.format(app=app_label) for perm in self.has_all_permissions
        ]
        self.has_any_permission = [
            perm.format(app=app_label) for perm in self.has_any_permission
        ]


class OnlyAnyPermissionView:
    models = [User]
    has_any_permission = ["{app}.change_user", "{app}.delete_user"]

    def __init__(self):
        app_label = User._meta.app_label  # noqa: SLF001
        self.has_any_permission = [
            perm.format(app=app_label) for perm in self.has_any_permission
        ]


class AdvancedDRFPermissionTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.permission_check = AdvancedDRFPermission()

        self.superuser = UserFactory(
            is_superuser=True, is_staff=True, email="admin@example.com"
        )
        self.regular_user = UserFactory(email="user@example.com")

        self.user_content_type = ContentType.objects.get_for_model(User)

        self.view_user_perm, _ = Permission.objects.get_or_create(
            codename="view_user",
            name="Can view user",
            content_type=self.user_content_type,
        )
        self.add_user_perm, _ = Permission.objects.get_or_create(
            codename="add_user",
            name="Can add user",
            content_type=self.user_content_type,
        )
        self.change_user_perm, _ = Permission.objects.get_or_create(
            codename="change_user",
            name="Can change user",
            content_type=self.user_content_type,
        )
        self.delete_user_perm, _ = Permission.objects.get_or_create(
            codename="delete_user",
            name="Can delete user",
            content_type=self.user_content_type,
        )

        self.view_group = Group.objects.create(name="ViewGroup")
        self.view_group.permissions.add(self.view_user_perm)

        self.add_group = Group.objects.create(name="AddGroup")
        self.add_group.permissions.add(self.add_user_perm)

        self.change_group = Group.objects.create(name="ChangeGroup")
        self.change_group.permissions.add(self.change_user_perm)

        self.delete_group = Group.objects.create(name="DeleteGroup")
        self.delete_group.permissions.add(self.delete_user_perm)

        self.regular_user.groups.clear()

    def test_superuser_get(self):
        request = self.factory.get("/")
        request.user = self.superuser
        assert self.permission_check.has_permission(request, MockUserView())

    def test_superuser_post(self):
        request = self.factory.post("/")
        request.user = self.superuser
        assert self.permission_check.has_permission(request, MockUserView())

    def test_superuser_put(self):
        request = self.factory.put("/")
        request.user = self.superuser
        assert self.permission_check.has_permission(request, MockUserView())

    def test_superuser_delete(self):
        request = self.factory.delete("/")
        request.user = self.superuser
        assert self.permission_check.has_permission(request, MockUserView())

    def test_superuser_patch(self):
        request = self.factory.patch("/")
        request.user = self.superuser
        assert self.permission_check.has_permission(request, MockUserView())

    def test_superuser_head(self):
        request = self.factory.head("/")
        request.user = self.superuser
        assert self.permission_check.has_permission(request, MockUserView())

    def test_superuser_options(self):
        request = self.factory.options("/")
        request.user = self.superuser
        assert self.permission_check.has_permission(request, MockUserView())

    def test_regular_user_no_permissions_get(self):
        request = self.factory.get("/")
        request.user = self.regular_user
        assert not self.permission_check.has_permission(request, MockUserView())

    def test_regular_user_no_permissions_post(self):
        request = self.factory.post("/")
        request.user = self.regular_user
        assert not self.permission_check.has_permission(request, MockUserView())

    def test_view_permission_allows_get(self):
        self.regular_user.groups.add(self.view_group)
        request = self.factory.get("/")
        request.user = self.regular_user
        assert self.permission_check.has_permission(request, MockUserView())

    def test_view_permission_denies_post(self):
        self.regular_user.groups.add(self.view_group)
        request = self.factory.post("/")
        request.user = self.regular_user
        assert not self.permission_check.has_permission(request, MockUserView())

    def test_add_permission_allows_post(self):
        self.regular_user.groups.add(self.add_group)
        request = self.factory.post("/")
        request.user = self.regular_user
        assert self.permission_check.has_permission(request, MockUserView())

    def test_add_permission_denies_get(self):
        self.regular_user.groups.add(self.add_group)
        request = self.factory.get("/")
        request.user = self.regular_user
        assert not self.permission_check.has_permission(request, MockUserView())

    def test_change_permission_allows_put(self):
        self.regular_user.groups.add(self.change_group)
        request = self.factory.put("/")
        request.user = self.regular_user
        assert self.permission_check.has_permission(request, MockUserView())

    def test_change_permission_allows_patch(self):
        self.regular_user.groups.add(self.change_group)
        request = self.factory.patch("/")
        request.user = self.regular_user
        assert self.permission_check.has_permission(request, MockUserView())

    def test_change_permission_denies_delete(self):
        self.regular_user.groups.add(self.change_group)
        request = self.factory.delete("/")
        request.user = self.regular_user
        assert not self.permission_check.has_permission(request, MockUserView())

    def test_delete_permission_allows_delete(self):
        self.regular_user.groups.add(self.delete_group)
        request = self.factory.delete("/")
        request.user = self.regular_user
        assert self.permission_check.has_permission(request, MockUserView())

    def test_delete_permission_denies_put(self):
        self.regular_user.groups.add(self.delete_group)
        request = self.factory.put("/")
        request.user = self.regular_user
        assert not self.permission_check.has_permission(request, MockUserView())

    def test_view_without_model_returns_false(self):
        request = self.factory.get("/")
        request.user = self.regular_user
        assert not self.permission_check.has_permission(request, MockNoModelView())

    def test_undefined_http_method_returns_false(self):
        request = self.factory.request(method="TRACE", path="/")
        request.user = self.regular_user
        assert not self.permission_check.has_permission(request, MockUserView())

    def test_custom_permissions_all_and_any_satisfied(self):
        self.regular_user.groups.add(self.view_group)
        self.regular_user.groups.add(self.add_group)
        self.regular_user.groups.add(self.change_group)
        request = self.factory.get("/")
        request.user = self.regular_user
        view = MockCustomPermissionsView()
        assert self.permission_check.has_permission(request, view)

    def test_custom_permissions_fail_and_condition(self):
        self.regular_user.groups.add(self.view_group)
        self.regular_user.groups.add(self.change_group)
        request = self.factory.get("/")
        request.user = self.regular_user
        view = MockCustomPermissionsView()
        assert not self.permission_check.has_permission(request, view)

    def test_only_or_permissions_succeed_when_present(self):
        self.regular_user.groups.add(self.change_group)
        request = self.factory.put("/")
        request.user = self.regular_user
        view = OnlyAnyPermissionView()
        assert self.permission_check.has_permission(request, view)

    def test_only_or_permissions_fail_when_absent(self):
        class OnlyAnyPermissionViewLocal:
            models = [User]
            has_any_permission = ["{app}.change_user", "{app}.delete_user"]

            def __init__(self):
                app_label = User._meta.app_label  # noqa: SLF001
                self.has_any_permission = [
                    perm.format(app=app_label) for perm in self.has_any_permission
                ]

        request = self.factory.get("/")
        request.user = self.regular_user
        view = OnlyAnyPermissionViewLocal()
        assert not self.permission_check.has_permission(request, view)
