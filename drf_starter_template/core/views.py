from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from drf_starter_template.utils.permissions import AdvancedDRFPermission


class BaseAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, AdvancedDRFPermission]

    # Define models for permission checks
    # List of model classes to check permissions against
    models = None

    # Custom permission lists:
    # List of permission strings where the user must have ALL listed permissions.
    has_all_permissions = []
    # List of permission strings where having any one of them is enough.
    has_any_permission = []

    # Define the mode for model permissions: "all" (default) means
    # the user must have permission on every model; "any" means at least one.
    model_permission_mode = "all"

    def get_model(self):
        return self.models
