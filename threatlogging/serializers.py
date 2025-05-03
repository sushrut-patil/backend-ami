from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import AccessLog, ActivityLog, ErrorLog, Threat


class AccessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessLog
        fields = '__all__'
        read_only_fields = ['id']  # Make id read-only since it's auto-generated


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = '__all__'
        read_only_fields = ['id']  # Make id read-only since it's auto-generated


class ErrorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorLog
        fields = '__all__'
        read_only_fields = ['id']  # Make id read-only since it's auto-generated


class ThreatSerializer(serializers.ModelSerializer):
    # Custom field to handle the log reference
    related_log_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Threat
        fields = ['id', 'log_type', 'content_type', 'object_id', 'description', 
                 'risk_score', 'detected_at', 'status', 'escalated', 
                 'resolved_by', 'resolved_at', 'related_log_id']
        read_only_fields = ['id', 'content_type', 'object_id']  # These are set based on log_type and related_log_id

    def create(self, validated_data):
        log_type = validated_data.get('log_type')
        related_log_id = validated_data.pop('related_log_id')
        
        # Map log_type to the corresponding model
        model_mapping = {
            'Access': AccessLog,
            'Activity': ActivityLog,
            'Error': ErrorLog,
        }
        
        model_class = model_mapping.get(log_type)
        if not model_class:
            raise serializers.ValidationError(f"Invalid log_type: {log_type}")
            
        content_type = ContentType.objects.get_for_model(model_class)
        
        # Verify the log exists
        try:
            model_class.objects.get(id=related_log_id)
        except model_class.DoesNotExist:
            raise serializers.ValidationError(f"No {log_type} log found with id {related_log_id}")
        
        # Create the threat with the correct content type and object id
        validated_data['content_type'] = content_type
        validated_data['object_id'] = related_log_id
        
        return super().create(validated_data)