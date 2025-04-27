from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdViewSet, RechargeRecordViewSet

router = DefaultRouter()
router.register(r'ads', AdViewSet)
router.register(r'recharge', RechargeRecordViewSet, basename='recharge')

urlpatterns = [
    path('', include(router.urls)),
]
