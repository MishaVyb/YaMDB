from rest_framework import permissions, views
from rest_framework.request import Request


class GetAnyOtherAdmin(permissions.BasePermission):
    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return request.method == 'GET' or (
            request.user.is_authenticated and request.user.is_admin
        )


class ListAnyOtherAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return request.method == 'GET' or (
            request.user.is_authenticated and request.user.is_admin
        )


class ReviewCommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        admin_or_moderator = request.user.is_authenticated and (
            request.user.is_admin or request.user.is_moderator
        )
        return (
            request.method == 'GET'
            or admin_or_moderator
            or request.user == obj.author
        )


class OnlyAdminPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: views.APIView):
        return request.user.is_authenticated and request.user.is_admin

class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        return request.user.is_authenticated and (
            request.user == obj.author
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )


class AdminOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsAdminOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == 'admin')
                or (request.user.is_authenticated
                    and request.user.is_superuser))

