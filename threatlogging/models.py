from django.db import models
from django.utils import timezone


class LogTypeChoices(models.TextChoices):
    ACCESS = "Access", "Access"
    ACTIVITY = "Activity", "Activity"
    ERROR = "Error", "Error"


class BaseLog(models.Model):
    """Abstract base model for all log types"""
    timestamp = models.DateTimeField(default=timezone.now)
    username = models.CharField(max_length=255,null=True)
    department = models.CharField(max_length=255,null=True)
    access_level = models.CharField(max_length=50, blank=True, null=True)  # e.g., "Admin", "User"
    system = models.CharField(max_length=100, blank=True, null=True)  # e.g., "CRM", "HRMS"
    message = models.TextField()

    class Meta:
        abstract = True


class AccessLog(BaseLog):
    """Model for tracking system access events"""
    action = models.CharField(max_length=100,null=True)  # e.g., "Login", "Logout"
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
    resource = models.CharField(max_length=255, blank=True, null=True)  # e.g., "Admin Panel"
    action = models.CharField(max_length=100, blank=True, null=True)  # e.g., "Viewed", "Deleted"
    status = models.CharField(max_length=50, blank=True, null=True)  # e.g., "Success", "Failed"
    justification = models.TextField(blank=True, null=True)  # Optional explanation

    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"

    def __str__(self):
        return f"{self.username} - {self.action} {self.resource} at {self.timestamp}"


class ErrorLog(BaseLog):
    """Model for tracking system errors"""
    error_type = models.CharField(max_length=100, blank=True, null=True)  # e.g., "PermissionError"
    stack_trace = models.TextField(blank=True, null=True)
    severity = models.CharField(max_length=50, blank=True, null=True)  # e.g., "Low", "Critical"
    originating_module = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Error Log"
        verbose_name_plural = "Error Logs"

    def __str__(self):
        return f"{self.error_type} - {self.username} at {self.timestamp}"