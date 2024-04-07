from rest_framework.permissions import BasePermission

class IsUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_user
        else:
            return False
        
class IsDriver(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff
        else:
            return False