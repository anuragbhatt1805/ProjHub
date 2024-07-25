from rest_framework import permissions


class IsSuperuserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read permissions for all requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only allow POST (create project) for superusers.
        return request.user.is_superuser or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Allow read permissions for all requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow PUT/PATCH (update project) for superusers and staff.
        return request.user.is_superuser or request.user.is_staff
