from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse


class Department(models.Model):
    """Department model"""
    dept_id = models.CharField(max_length=10, unique=True, primary_key=True)
    dept_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dept_id} - {self.dept_name}"

    def get_absolute_url(self):
        return reverse('department-detail', kwargs={'pk': self.dept_id})

    class Meta:
        ordering = ['dept_id']

class AccessLevel(models.Model):
    """Access level model"""
    access_id = models.CharField(max_length=10, unique=True, primary_key=True)
    access_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Risk score from 1-100
    risk_score = models.IntegerField(default=0, help_text="Risk score from 1-100")
    
    def __str__(self):
        return f"{self.access_id} - {self.access_name}"

    def get_absolute_url(self):
        return reverse('access-detail', kwargs={'pk': self.access_id})

    class Meta:
        ordering = ['access_id']

class Employee(models.Model):
    """Employee model"""
    employee_id = models.CharField(max_length=10, unique=True, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    access_levels = models.ManyToManyField(AccessLevel, through='EmployeeAccess', related_name='employees')
    job_title = models.CharField(max_length=100, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('employee-detail', kwargs={'pk': self.employee_id})
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def risk_score(self):
        """Calculate employee risk score based on access levels"""
        if not self.access_levels.exists():
            return 0
        
        return sum(level.risk_score for level in self.access_levels.all()) / self.access_levels.count()

    class Meta:
        ordering = ['last_name', 'first_name']

class EmployeeAccess(models.Model):
    """Model to represent the many-to-many relationship between employees and access levels"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE)
    granted_date = models.DateField(auto_now_add=True)
    granted_by = models.CharField(max_length=100, blank=True, null=True)
    revoked_date = models.DateField(blank=True, null=True)
    revoked_by = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee} - {self.access_level}"
    
    class Meta:
        unique_together = ('employee', 'access_level')
        verbose_name_plural = 'Employee Access Rights'


class AccessAuditLog(models.Model):
    """Model to track changes to employee access levels"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='audit_logs')
    access_level = models.ForeignKey(AccessLevel, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)  # 'granted', 'revoked', 'modified'
    action_by = models.CharField(max_length=100)
    action_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.action} - {self.employee} - {self.access_level}"
    
    class Meta:
        ordering = ['-action_date']
