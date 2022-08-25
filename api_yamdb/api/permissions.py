from rest_framework import permissions, SAFE_METHODS

from users.models import User


class ListAnyOtherAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                 and request.user.role == 'admin')
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and request.user.role == 'admin')


class GetAnyOtherAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                 and request.user.role == 'admin')
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return request.method == 'GET' or (request.user.is_authenticated
                                           and request.user.role == 'admin')


class ReviewCommentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (request.user.is_superuser
                or request.user.role in ('admin', 'moderator')
                or obj.author == request.user
                or request.method in permissions.SAFE_METHODS)
