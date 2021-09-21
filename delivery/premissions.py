from rest_framework.permissions import BasePermission


class CustomerOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "customer")


class RestaurateurOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "restaurateur")
            and request.user.restaurateur.is_owner
            or request.user.restaurateur.is_manager
        )


class CourierOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "courier")


class CustomerAndRestaurateurOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                hasattr(request.user, "customer")
                or (
                        hasattr(request.user, "restaurateur")
                        and request.user.restaurateur.is_active
                        and request.user.restaurateur.is_manager
                )
        )
