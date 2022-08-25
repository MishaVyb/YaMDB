from rest_framework import permissions, SAFE_METHODS

from users.models import User


class IsAdminOrReadonlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif (
                request.user.is_authenticated
                and request.user.role == 'admin'):
            return True


class TestPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser


class ReviewCommentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_superuser
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or obj.author == request.user
                or request.method in permissions.SAFE_METHODS)

