from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method == 'POST' and not request.user.is_superuser:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id

    def has_permission(self, request, view):
        if request.method == 'POST' and not request.user.is_superuser:
            return False
        return True
