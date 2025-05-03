from django.contrib import admin
from .models import Department, AccessLevel, Employee, EmployeeAccess, AccessAuditLog


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_id', 'dept_name', 'created_at')
    search_fields = ('dept_id', 'dept_name')


@admin.register(AccessLevel)
class AccessLevelAdmin(admin.ModelAdmin):
    list_display = ('access_id', 'access_name', 'risk_score', 'created_at')
    search_fields = ('access_id', 'access_name')
    list_filter = ('risk_score',)


class EmployeeAccessInline(admin.TabularInline):
    model = EmployeeAccess
    extra = 1
    fields = ('access_level', 'granted_date', 'granted_by', 'is_active')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'first_name', 'last_name', 'email', 'department', 'job_title')
    search_fields = ('employee_id', 'first_name', 'last_name', 'email')
    list_filter = ('department', 'hire_date')
    inlines = [EmployeeAccessInline]


@admin.register(EmployeeAccess)
class EmployeeAccessAdmin(admin.ModelAdmin):
    list_display = ('employee', 'access_level', 'granted_date', 'is_active')
    search_fields = ('employee__first_name', 'employee__last_name', 'access_level__access_name')
    list_filter = ('is_active', 'granted_date', 'revoked_date')


@admin.register(AccessAuditLog)
class AccessAuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'employee', 'access_level', 'action_by', 'action_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'access_level__access_name')
    list_filter = ('action', 'action_date')
    readonly_fields = ('employee', 'access_level', 'action', 'action_by', 'action_date')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
