from rest_framework import permissions

class CanCreateInvoice(permissions.BasePermission):
    def has_permission(self, request, view):
        # 只有普通用户可以创建
        return request.user.is_authenticated and request.user.role == 'user'

class CanReviewInvoice(permissions.BasePermission):
    def has_permission(self, request, view):
        # 管理员才可以访问审核接口
        return request.user.is_authenticated and request.user.role == 'admin'