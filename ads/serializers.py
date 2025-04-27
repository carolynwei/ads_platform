from rest_framework import serializers
from .models import Ad
from .models import RechargeRecord

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'advertiser', 'ad_type', 'title', 'description', 'image_url', 'video_url', 'target_page', 'start_date', 'end_date', 'status', 'created_at']
        read_only_fields = ['advertiser', 'created_at']

class AdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['ad_type', 'title', 'description', 'image_url', 'video_url', 'target_page', 'start_date', 'end_date']


class RechargeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RechargeRecord
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'status']
