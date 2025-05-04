from django.db import models

class Compliance(models.Model):
    """Model for managing compliance requirements"""
    CATEGORY_CHOICES = [
        ('GDPR', 'General Data Protection Regulation'),
        ('HIPAA', 'Health Insurance Portability and Accountability Act'),
        ('PCI-DSS', 'Payment Card Industry Data Security Standard'),
        ('SOX', 'Sarbanes-Oxley Act'),
        ('ISO27001', 'ISO 27001'),
        ('NIST', 'National Institute of Standards and Technology'),
        ('CCPA', 'California Consumer Privacy Act'),
        ('OTHER', 'Other')
    ]
    
    STATUS_CHOICES = [
        ('COMPLIANT', 'Compliant'),
        ('NON_COMPLIANT', 'Non-Compliant'),
        ('IN_PROGRESS', 'In Progress'),
        ('NOT_APPLICABLE', 'Not Applicable'),
        ('NEEDS_REVIEW', 'Needs Review')
    ]
    
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    requirements = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEEDS_REVIEW')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} - {self.category} - {self.status}"