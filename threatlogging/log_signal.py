from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AccessLog, ActivityLog, ErrorLog
from .threat_analysis import process_log_entry

@receiver(post_save, sender=AccessLog)
def detect_threat_from_access_log(sender, instance, created, **kwargs):
    if created:
        print("H")
        process_log_entry(instance, "Access")

@receiver(post_save, sender=ActivityLog)
def detect_threat_from_activity_log(sender, instance, created, **kwargs):
    if created:
        process_log_entry(instance, "Activity")

@receiver(post_save, sender=ErrorLog)
def detect_threat_from_error_log(sender, instance, created, **kwargs):
    if created:
        process_log_entry(instance, "Error")
