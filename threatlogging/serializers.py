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
        # Remove the problematic field from the explicit fields list
        fields = ['id', 'log_type', 'description', 'risk_score', 
                 'detected_at', 'status', 'escalated', 'resolved_by', 
                 'resolved_at', 'related_log_id']
        read_only_fields = ['id']  # We'll handle content_type & object_id separately

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
        
        # Create the threat instance first
        threat = Threat(**validated_data)
        
        # Then set the content_type and object_id attributes directly
        # This approach works regardless of the actual field name
        threat.content_type = content_type
        threat.object_id = related_log_id
        
        # Save the new threat
        threat.save()
        
        return threat