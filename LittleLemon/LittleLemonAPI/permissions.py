from rest_framework.permissions import BasePermission


class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists()


class IsDeliveryUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='delivery_crew').exists()


class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return len(request.user.groups.all()) == 0


class IsManagerOrDeliveryUser(BasePermission):
    def has_permission(self, request, view):
        return IsManagerUser().has_permission(request, view) or IsDeliveryUser().has_permission(request, view)


class IsManagerOrDeliveryOrCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return IsManagerUser().has_permission(request, view) \
               or IsDeliveryUser().has_permission(request, view)\
               or IsCustomerUser().has_permission(request, view)
