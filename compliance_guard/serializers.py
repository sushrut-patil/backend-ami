from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Compliance

class ComplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compliance
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']