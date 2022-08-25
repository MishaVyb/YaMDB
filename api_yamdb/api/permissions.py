from rest_framework import permissions, SAFE_METHODS

from users.models import User


class IsAdminOrReadonlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
<<<<<<< HEAD
=======
        elif request.user.is_authenticated and request.user.role=='admin':
            return True


class IsAdminOrReadonly(BasePermission):

    def has_permission(self, request, view):

        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin')



class AuthorAdminModeratorPermission(permissions.BasePermission):
>>>>>>> 1aa63e14caebc19aeeb409fccf418c398539c0ec

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif (
                request.user.is_authenticated

                and request.user.role == 'admin'):
            return True
<<<<<<< HEAD
=======
        elif (
                request.user.is_authenticated
                and request.user.role == 'moderator'

        ):
            return True
>>>>>>> 1aa63e14caebc19aeeb409fccf418c398539c0ec


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
        return request.user.is_authenticated and (request.user.is_superuser
                or request.user.role in ('admin', 'moderator')
                or obj.author == request.user
                or request.method in permissions.SAFE_METHODS)
