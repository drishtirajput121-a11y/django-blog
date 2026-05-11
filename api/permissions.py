from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission:
    - GET/HEAD/OPTIONS → allowed for anyone
    - PUT/PATCH/DELETE → only the author/owner of the object
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in SAFE_METHODS:
            return True
        # Write permissions only for the owner
        # Works for Blog (obj.author) and Comment (obj.user)
        return getattr(obj, 'author', None) == request.user or \
               getattr(obj, 'user', None) == request.user
