from rest_framework import serializers
from .models import AccessLog, ActivityLog, ErrorLog


class AccessLogSerializer(serializers.ModelSerializer):
    """Serializer for AccessLog model"""
    class Meta:
        model = AccessLog
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']


class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for ActivityLog model"""
    class Meta:
        model = ActivityLog
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']


class ErrorLogSerializer(serializers.ModelSerializer):
    """Serializer for ErrorLog model"""
    class Meta:
        model = ErrorLog
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']

from .models import Threat
class ThreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threat
        fields = '__all__'
        read_only_fields = ['detected_at']
