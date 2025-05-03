from rest_framework import serializers
from .models import Department, AccessLevel, Employee, EmployeeAccess, AccessAuditLog


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class AccessLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessLevel
        fields = '__all__'


class EmployeeAccessSerializer(serializers.ModelSerializer):
    access_level_name = serializers.CharField(source='access_level.access_name', read_only=True)
    
    class Meta:
        model = EmployeeAccess
        fields = ['id', 'employee', 'access_level', 'access_level_name', 'granted_date', 
                  'granted_by', 'revoked_date', 'revoked_by', 'is_active', 'notes']


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.dept_name', read_only=True)
    access_levels = AccessLevelSerializer(many=True, read_only=True)
    risk_score = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'full_name', 'email', 
                  'department', 'department_name', 'job_title', 'hire_date', 
                  'access_levels', 'risk_score', 'created_at', 'updated_at']


class EmployeeDetailSerializer(EmployeeSerializer):
    employee_access = EmployeeAccessSerializer(source='employeeaccess_set', many=True, read_only=True)
    
    class Meta(EmployeeSerializer.Meta):
        fields = EmployeeSerializer.Meta.fields + ['employee_access']


class AccessAuditLogSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    access_level_name = serializers.CharField(source='access_level.access_name', read_only=True)
    
    class Meta:
        model = AccessAuditLog
        fields = ['id', 'employee', 'employee_name', 'access_level', 'access_level_name',
                  'action', 'action_by', 'action_date', 'notes']