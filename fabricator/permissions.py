from rest_framework import permissions

class UpdateFabricator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'PUT':
            if request.user.is_superuser or request.user.is_staff:
                return True
            else:
                return False
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method == 'PUT' and not request.user.is_superuser:
            return False
        return request.method in permissions.SAFE_METHODS