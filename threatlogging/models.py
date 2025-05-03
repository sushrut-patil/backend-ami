from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class LogTypeChoices(models.TextChoices):
    ACCESS = "Access", "Access"
    ACTIVITY = "Activity", "Activity"
    ERROR = "Error", "Error"


class BaseLog(models.Model):
    """Abstract base model for all log types"""
    id = models.AutoField(
        primary_key=True)  # Explicitly defining auto-incrementing ID
    timestamp = models.DateTimeField(default=timezone.now)
    username = models.CharField(max_length=255, null=True)
    department = models.CharField(max_length=255, null=True)
    access_level = models.CharField(
        max_length=50, blank=True, null=True)  # e.g., "Admin", "User"
    system = models.CharField(
        max_length=100, blank=True, null=True)  # e.g., "CRM", "HRMS"
    message = models.TextField()

    class Meta:
        abstract = True


class AccessLog(BaseLog):
    """Model for tracking system access events"""
    action = models.CharField(
        max_length=100, null=True)  # e.g., "Login", "Logout"
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    device = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Access Log"
        verbose_name_plural = "Access Logs"

    def __str__(self):
        return f"{self.username} - {self.action} at {self.timestamp}"


class ActivityLog(BaseLog):
    """Model for tracking user activities within the system"""
    resource = models.CharField(
        max_length=255, blank=True, null=True)  # e.g., "Admin Panel"
    # e.g., "Viewed", "Deleted"
    action = models.CharField(max_length=100, blank=True, null=True)
    # e.g., "Success", "Failed"
    status = models.CharField(max_length=50, blank=True, null=True)
    justification = models.TextField(
        blank=True, null=True)  # Optional explanation

    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"

    def __str__(self):
        return f"{self.username} - {self.action} {self.resource} at {self.timestamp}"


class ErrorLog(BaseLog):
    """Model for tracking system errors"""
    error_type = models.CharField(
        max_length=100, blank=True, null=True)  # e.g., "PermissionError"
    stack_trace = models.TextField(blank=True, null=True)
    # e.g., "Low", "Critical"
    severity = models.CharField(max_length=50, blank=True, null=True)
    originating_module = models.CharField(
        max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Error Log"
        verbose_name_plural = "Error Logs"

    def __str__(self):
        return f"{self.error_type} - {self.username} at {self.timestamp}"


class ThreatStatus(models.TextChoices):
    NEW = "New", "New"
    ESCALATED = "Escalated", "Escalated"
    RESOLVED = "Resolved", "Resolved"
    UNDER_INVESTIGATION = "Under Investigation", "Under Investigation"


# If you prefer not to migrate the database schema, you can modify your Threat model instead:


class ThreatStatus(models.TextChoices):
    NEW = "New", "New"
    ESCALATED = "Escalated", "Escalated"
    RESOLVED = "Resolved", "Resolved"
    UNDER_INVESTIGATION = "Under Investigation", "Under Investigation"


class LogTypeChoices(models.TextChoices):
    ACCESS = "Access", "Access"
    ACTIVITY = "Activity", "Activity"
    ERROR = "Error", "Error"


class Threat(models.Model):
    """Model for tracking security threats based on log entries"""
    id = models.AutoField(primary_key=True)
    log_type = models.CharField(max_length=50, choices=LogTypeChoices.choices)

    # Replace ContentType framework with a simple log_id field
    log_id = models.PositiveIntegerField()

    description = models.TextField()
    risk_score = models.FloatField(default=0.0)
    detected_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=50, choices=ThreatStatus.choices, default=ThreatStatus.NEW)
    escalated = models.BooleanField(default=False)
    resolved_by = models.CharField(max_length=255, blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Threat"
        verbose_name_plural = "Threats"

    def __str__(self):
        return f"{self.log_type} Threat (ID: {self.id}) - {self.status}"

    # You can add methods to retrieve the associated log if needed
    def get_log(self):
        """Get the associated log entry based on log_type"""
        if self.log_type == LogTypeChoices.ACCESS:
            from .models import AccessLog
            return AccessLog.objects.filter(id=self.log_id).first()
        elif self.log_type == LogTypeChoices.ACTIVITY:
            from .models import ActivityLog
            return ActivityLog.objects.filter(id=self.log_id).first()
        elif self.log_type == LogTypeChoices.ERROR:
            from .models import ErrorLog
            return ErrorLog.objects.filter(id=self.log_id).first()
        return None
