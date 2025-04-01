from rest_framework.permissions import BasePermission, SAFE_METHODS
from AIRPORT_MANAGER.models import CrewMember

class IsAdminOrInspectorForWrite(BasePermission):
    """
    Позволява само на логнати потребители с роля 'Admin' или 'Inspector' да пишат.
    Всички могат да четат.
    """

    def has_permission(self, request, view):
        # Позволява четене на всички
        if request.method in SAFE_METHODS:
            return True

        # Позволява писане само ако потребителят е логнат и има роля
        user = request.user
        if user and user.is_authenticated and hasattr(user, 'role'):
            return user.role.name in ['Admin', 'Inspector']
        return False


class IsCrewUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            CrewMember.objects.filter(user=request.user).exists()
        )