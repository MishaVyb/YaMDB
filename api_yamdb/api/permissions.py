from rest_framework import permissions

from users.models import User


class AdminOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated and request.user.is_admin:
            return True


class AdminOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_superuser:
            return True
        elif request.user.is_authenticated and request.user.is_admin:
            return True

class AuthorAdminModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif obj.author == request.user:
            return True
        elif request.user.is_superuser:
            return True
        elif (
                request.user.is_authenticated
                and request.user.is_admin):
            return True
        elif (
                request.user.is_authenticated
                and request.user.is_moderator
        ):
            return True



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

