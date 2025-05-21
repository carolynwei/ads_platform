# ads/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from django.db import models
from django.conf import settings

User = get_user_model()

class Ad(models.Model):
    # 广告类型
    AD_TYPE_CHOICES = (
        ('banner', 'Banner'),
        ('interstitial', 'Interstitial'),
        ('video', 'Video'),
    )

    # 广告状态
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('stopped', 'Stopped'),
    )

    # 计费方式
    BILLING_METHOD_CHOICES = (
        ('CPM', '按展示计费'),
        ('CPC', '按点击计费'),
        ('CPT', '按时长计费'),
    )

    # 基本信息
    advertiser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ads")
    billing_method = models.CharField(max_length=10, choices=BILLING_METHOD_CHOICES, default='CPM')
    ad_type = models.CharField(max_length=20, choices=AD_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    target_page = models.URLField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    # 审核相关
    reason_rejected = models.TextField(null=True, blank=True)

    # 统计字段
    display_count = models.PositiveIntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    # 价格设置
    cpm_price = models.DecimalField(default=10.00, max_digits=6, decimal_places=2)  # 每千次展示费用
    cpc_price = models.DecimalField(default=1.00, max_digits=6, decimal_places=2)   # 每次点击费用
    cpt_price = models.DecimalField(default=2.00, max_digits=6, decimal_places=2)   # 每单位时间费用
    cpt_unit_seconds = models.PositiveIntegerField(default=10)  # 默认10秒为一个计费单位

    # 状态字段
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # 根据status字段来动态设置is_active
        if self.status in ['approved']:
            self.is_active = True
        else:
            self.is_active = False
        super().save(*args, **kwargs)

    # ✅ 封装常用逻辑方法
    def increment_display(self):
        self.display_count = models.F('display_count') + 1
        self.save(update_fields=['display_count'])

    def increment_click(self):
        self.click_count = models.F('click_count') + 1
        self.save(update_fields=['click_count'])

    def charge(self, amount):
        """通用扣费函数，用于 CPM/CPC/CPT 三种方式"""
        if self.advertiser.balance >= amount:
            self.advertiser.balance -= amount
            self.advertiser.save()
            self.total_spent += amount
            self.save(update_fields=['total_spent'])
            return True
        else:
            # 余额不足，暂停广告
            self.is_active = False
            self.save(update_fields=['is_active'])
            return False

    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
        ordering = ['-created_at']
    
class ThirdPartyAdMetrics(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    developer = models.ForeignKey(User, on_delete=models.CASCADE)  # 如果有自定义User就用自定义的
    click_count = models.IntegerField(default=0)
    view_duration_seconds = models.IntegerField(default=0)
    impression_count = models.IntegerField(default=0)
    reported_at = models.DateTimeField(auto_now_add=True)

class AdInteraction(models.Model):
    ACTION_CHOICES = (
        ('display', 'Display'),
        ('click', 'Click'),
        ('watch', 'Watch'),  # ✅ 用于 CPT 模式
    )

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # ✅ 新增字段：播放时长（单位：秒），仅适用于 CPT 模式
    duration = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.ad.title} - {self.action} @ {self.timestamp}"


class RechargeRecord(models.Model):
    PAYMENT_CHOICES = [
        ('wechat', 'WeChat Pay'),
        ('alipay', 'Alipay'),
        ('bank', 'Bank Transfer'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recharges')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success')  # 模拟成功
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount} 元'

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('pending', '待开票'),
        ('issued', '已开票'),
        ('rejected', '已驳回'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, help_text="发票抬头")
    tax_number = models.CharField(max_length=50, help_text="税号")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="开票金额")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    pdf_file = models.FileField(upload_to='invoices/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.amount} - {self.status}"
