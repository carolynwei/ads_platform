from django.contrib import admin
from .models import Ad, ThirdPartyAdMetrics, AdInteraction, RechargeRecord

# 自定义 Ad 管理界面
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'advertiser', 'ad_type', 'status', 'start_date', 'end_date', 'is_active', 'total_spent')
    list_filter = ('ad_type', 'status', 'is_active')
    search_fields = ('title', 'advertiser__username', 'description')
    list_editable = ('status', 'is_active')
    ordering = ('-created_at',)

admin.site.register(Ad, AdAdmin)

# ThirdPartyAdMetrics 管理界面
class ThirdPartyAdMetricsAdmin(admin.ModelAdmin):
    list_display = ('ad', 'developer', 'click_count', 'view_duration_seconds', 'impression_count', 'reported_at')
    search_fields = ('ad__title', 'developer__username')
    list_filter = ('developer',)

admin.site.register(ThirdPartyAdMetrics, ThirdPartyAdMetricsAdmin)

# AdInteraction 管理界面
class AdInteractionAdmin(admin.ModelAdmin):
    list_display = ('ad', 'user', 'action', 'timestamp', 'duration')
    list_filter = ('action', 'timestamp')
    search_fields = ('ad__title', 'user__username')

admin.site.register(AdInteraction, AdInteractionAdmin)

# RechargeRecord 管理界面
class RechargeRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('payment_method', 'status')
    search_fields = ('user__username',)

admin.site.register(RechargeRecord, RechargeRecordAdmin)

class AdInteractionInline(admin.TabularInline):
    model = AdInteraction
    extra = 1  # 额外添加一个空白表单

class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'advertiser', 'ad_type', 'status', 'start_date', 'end_date', 'is_active', 'total_spent')
    inlines = [AdInteractionInline]  # 将 AdInteraction 嵌入到 Ad 后台

from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['client', 'title', 'amount', 'status', 'created_at']
    list_filter = ['status']