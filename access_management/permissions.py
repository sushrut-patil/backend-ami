from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow administrators to edit objects.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to admin users
        return request.user and request.user.is_staff


class IsAccessManager(permissions.BasePermission):
    """
    Custom permission for access management operations.
    Only users with proper permissions can modify access levels.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Check if user has access_management permission
        return request.user and (
            request.user.is_staff or 
            request.user.has_perm('access_management.add_employeeaccess') or
            request.user.has_perm('access_management.change_employeeaccess')
        )