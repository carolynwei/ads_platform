# users/permissions.py
from rest_framework import permissions

class IsRealAdmin(permissions.BasePermission):
    """
    只有角色为 'admin' 的用户才有权限。
    用于代替 DRF 默认的 IsAdminUser。
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin'


class IsClient(permissions.BasePermission):
    """
    只有角色为 'client' 的用户才有权限。
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'client'

class IsAdminOrClient(permissions.BasePermission):
    """
    只有 'admin' 或 'client' 角色的用户可以访问。
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', '') in ['admin', 'client']

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    只有广告的创建者（client）或管理员（admin）才有权限修改广告。
    """
    def has_object_permission(self, request, view, obj):
        # 允许 admin 执行所有操作，或广告的创建者执行修改操作
        return request.user.is_authenticated and (request.user == obj.advertiser or request.user.role == 'admin')
