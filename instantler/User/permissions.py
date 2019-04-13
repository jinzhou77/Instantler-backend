from rest_framework import permissions
from django.contrib.auth.models import User

class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return request.method in ("GET", "HEAD") or request.user.id == obj.id
        else:
            return False
