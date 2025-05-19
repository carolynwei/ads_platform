from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdViewSet, RechargeRecordViewSet,InvoiceViewSet
from . import views

router = DefaultRouter()
router.register(r'ads', AdViewSet)
router.register(r'recharge', RechargeRecordViewSet, basename='recharge')

urlpatterns = [
    path('', include(router.urls)),
    path('recharge-history/', views.recharge_history, name='recharge_history'),
    path('recharge-history/export/', views.export_recharge_history, name='export_recharge_history'),
]


router.register(r'invoices', InvoiceViewSet)

urlpatterns += router.urls  # 若有其他 urlpatterns，请合并使用：urlpatterns += router.urls
