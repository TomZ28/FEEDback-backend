from rest_framework import permissions
from rest_framework.permissions import BasePermission

# Code is adapted from django rest framework documentation: https://www.django-rest-framework.org/api-guide/permissions/#examples
class IsRestaurantOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.

    Source: https://www.django-rest-framework.org/api-guide/permissions/#examples
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or not hasattr(obj, 'owner'):
            return True

        return obj.owner == request.user