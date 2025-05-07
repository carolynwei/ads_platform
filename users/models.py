# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('admin', 'Admin'),
        ('third_party', 'Third-Party Dev'),   # 第三方开发者
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='client')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 新增余额字段
    created_at = models.DateTimeField(auto_now_add=True)
    is_profile_completed = models.BooleanField(default=False)
    company = models.CharField(max_length=100, blank=True, null=True)  # 添加公司字段
    
    def __str__(self):
        return f"{self.username} ({self.role})"
