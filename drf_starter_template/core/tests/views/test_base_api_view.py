from django.test import TestCase
from rest_framework.permissions import IsAuthenticated

from drf_starter_template.core.views import BaseAPIView
from drf_starter_template.utils.permissions import AdvancedDRFPermission


class DummyView(BaseAPIView):
    models = ["model1", "model2"]
    has_all_permissions = ["perm1", "perm2"]
    has_any_permission = ["perm3", "perm4"]
    model_permission_mode = "any"


class BaseAPIViewTests(TestCase):
    def test_permission_classes(self):
        expected_permissions = [IsAuthenticated, AdvancedDRFPermission]
        assert BaseAPIView.permission_classes == expected_permissions

    def test_get_model_default(self):
        view = BaseAPIView()
        assert view.get_model() is None

    def test_get_model_when_set(self):
        view = DummyView()
        assert view.get_model() == ["model1", "model2"]

    def test_default_attributes(self):
        view = BaseAPIView()
        assert view.models is None
        assert view.has_all_permissions == []
        assert view.has_any_permission == []
        assert view.model_permission_mode == "all"

    def test_custom_attributes(self):
        view = DummyView()
        assert view.models == ["model1", "model2"]
        assert view.has_all_permissions == ["perm1", "perm2"]
        assert view.has_any_permission == ["perm3", "perm4"]
        assert view.model_permission_mode == "any"
