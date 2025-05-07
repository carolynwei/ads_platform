# users/serializers.py

from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)  # 加了角色选择
    company = serializers.CharField(required=False, allow_blank=True, max_length=100)  # 新增字段
    
    class Meta:
        model = User
        fields = ('username','company', 'email', 'password', 'password2', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "两次密码输入不一致"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # 不需要存 password2
        password = validated_data.pop('password')
        
        user = User(**validated_data)
        user.set_password(password)  # 正确加密密码
        user.save()
        return user