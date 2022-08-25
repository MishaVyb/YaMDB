from rest_framework import permissions


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
