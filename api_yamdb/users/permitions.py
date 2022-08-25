from rest_framework import permissions, views
from rest_framework.request import Request


class AdminUserPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: views.APIView):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )
