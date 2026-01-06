from rest_framework.permissions import BasePermission


class IsGerant(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return hasattr(request.user, "gerant_profile")

    # app/permissions.py


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, "client_profile")
        )
