import django_filters
from .models import Department, AccessLevel, Employee, EmployeeAccess, AccessAuditLog


class DepartmentFilter(django_filters.FilterSet):
    class Meta:
        model = Department
        fields = {
            'dept_id': ['exact', 'icontains'],
            'dept_name': ['exact', 'icontains'],
            'created_at': ['gte', 'lte'],
        }


class AccessLevelFilter(django_filters.FilterSet):
    class Meta:
        model = AccessLevel
        fields = {
            'access_id': ['exact', 'icontains'],
            'access_name': ['exact', 'icontains'],
            'risk_score': ['exact', 'gte', 'lte'],
            'created_at': ['gte', 'lte'],
        }


class EmployeeFilter(django_filters.FilterSet):
    department = django_filters.CharFilter(field_name='department__dept_id')
    hire_date_from = django_filters.DateFilter(field_name='hire_date', lookup_expr='gte')
    hire_date_to = django_filters.DateFilter(field_name='hire_date', lookup_expr='lte')
    risk_score_min = django_filters.NumberFilter(field_name='risk_score', lookup_expr='gte')
    risk_score_max = django_filters.NumberFilter(field_name='risk_score', lookup_expr='lte')
    
    class Meta:
        model = Employee
        fields = {
            'employee_id': ['exact', 'icontains'],
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'job_title': ['exact', 'icontains'],
            'created_at': ['gte', 'lte'],
        }


class EmployeeAccessFilter(django_filters.FilterSet):
    employee = django_filters.CharFilter(field_name='employee__employee_id')
    access_level = django_filters.CharFilter(field_name='access_level__access_id')
    granted_date_from = django_filters.DateFilter(field_name='granted_date', lookup_expr='gte')
    granted_date_to = django_filters.DateFilter(field_name='granted_date', lookup_expr='lte')
    revoked_date_from = django_filters.DateFilter(field_name='revoked_date', lookup_expr='gte')
    revoked_date_to = django_filters.DateFilter(field_name='revoked_date', lookup_expr='lte')
    
    class Meta:
        model = EmployeeAccess
        fields = ['is_active']


class AccessAuditLogFilter(django_filters.FilterSet):
    employee = django_filters.CharFilter(field_name='employee__employee_id')
    access_level = django_filters.CharFilter(field_name='access_level__access_id')
    action_date_from = django_filters.DateTimeFilter(field_name='action_date', lookup_expr='gte')
    action_date_to = django_filters.DateTimeFilter(field_name='action_date', lookup_expr='lte')
    
    class Meta:
        model = AccessAuditLog
        fields = ['action', 'action_by']