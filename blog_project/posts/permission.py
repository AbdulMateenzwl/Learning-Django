from rest_framework.permissions import BasePermission
from django.conf import settings

class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        # Determine user role
        if request.user.is_superuser:
            role = "ADMIN"
        elif request.user.is_staff:
            role = "STAFF"
        else:
            role = "USER"

        # Get allowed methods for this role
        allowed_methods = settings.CUSTOM_ROLE_PERMISSIONS.get(role, [])

        # Check if this HTTP method is allowed
        return request.method in allowed_methods
