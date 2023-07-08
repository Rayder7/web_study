from rest_framework.permissions import SAFE_METHODS, BasePermission


class CuratorPermission(BasePermission):
    """Куратор может управлять студентами и учебными группами"""

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.curator == request.user)