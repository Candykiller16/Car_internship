from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsCustomerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_customer:
            return True


class IsShowroomUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_showroom:
            return True


class IsDealerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_dealer:
            return True
