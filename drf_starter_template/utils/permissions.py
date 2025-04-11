from rest_framework import permissions


class AdvancedDRFPermission(permissions.BasePermission):
    method_permission_map = {
        "GET": "view",
        "POST": "add",
        "PUT": "change",
        "PATCH": "change",
        "DELETE": "delete",
        "HEAD": "view",
        "OPTIONS": "view",
    }

    def _check_all_permissions(self, user, perms):
        return all(user.has_perm(perm) for perm in perms)

    def _check_any_permission(self, user, perms):
        return any(user.has_perm(perm) for perm in perms)

    def _check_model_permissions(self, user, models, request, mode):
        action = self.method_permission_map.get(request.method)
        if not action:
            return False

        if not isinstance(models, (list, tuple)):
            models = [models]

        if not models:
            return False

        perms = []
        for model in models:
            meta = model._meta  # noqa: SLF001
            perm = f"{meta.app_label}.{action}_{meta.model_name}"
            perms.append(perm)

        if mode == "all":
            return all(user.has_perm(perm) for perm in perms)

        if mode == "any":
            return any(user.has_perm(perm) for perm in perms)

        return False

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True

        required_all = getattr(view, "has_all_permissions", [])
        required_any = getattr(view, "has_any_permission", [])
        models = getattr(view, "models", None)

        if not (required_all or required_any or models):
            return False

        allowed = True

        if required_all and not self._check_all_permissions(user, required_all):
            allowed = False

        if required_any and not self._check_any_permission(user, required_any):
            allowed = False

        if models:
            mode = getattr(view, "model_permission_mode", "all")
            if not self._check_model_permissions(user, models, request, mode):
                allowed = False

        return allowed
