from rest_framework import permissions


class GetAnyOtherAdmin(permissions.BasePermission):
    def has_permission(self, request, view):

        return ((request.user.is_authenticated
                 and request.user.role == 'admin')
                or request.user.is_superuser
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (request.method == 'GET'
                or (request.user.is_authenticated
                    and request.user.role == 'admin')
                or request.user.is_superuser)


class ListAnyOtherAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                 and request.user.role == 'admin')
                or request.user.is_superuser
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (request.method == 'GET'
                or (request.user.is_authenticated
                    and request.user.role == 'admin')
                or request.user.is_superuser)


class ReviewCommentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (request.method == 'GET'
                or (request.user.is_authenticated
                    and request.user.role in ('admin', 'moderator'))
                or request.user.is_superuser
                or request.user == obj.author)
