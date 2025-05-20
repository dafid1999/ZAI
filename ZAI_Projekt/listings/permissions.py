from rest_framework import permissions

class IsOwnerOrAdminOrModerator(permissions.BasePermission):
    """
    Allow read-only for all.
    Allow edit/delete if user is:
      - author of the listing
      - staff or superuser
      - member of 'moderators' group
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if obj.author == user:
            return True
        if user.is_staff or user.is_superuser:
            return True
        return user.groups.filter(name='moderators').exists()