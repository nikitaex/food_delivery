from rest_framework.permissions import BasePermission


class CustomerOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "customer")


class RestaurateurOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_restaurateur
        )


class CourierOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_courier


class CustomerAndRestaurateurOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                hasattr(request.user, "customer")
                or request.user.is_restaurateur
        )
