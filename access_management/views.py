from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Department, AccessLevel, Employee, EmployeeAccess, AccessAuditLog
from .filters import (
    DepartmentFilter, AccessLevelFilter, EmployeeFilter, 
    EmployeeAccessFilter, AccessAuditLogFilter
)
from .serializers import (
    DepartmentSerializer,
    AccessLevelSerializer,
    EmployeeSerializer,
    EmployeeDetailSerializer,
    EmployeeAccessSerializer,
    AccessAuditLogSerializer
)


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Department CRUD operations.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'dept_id'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DepartmentFilter
    search_fields = ['dept_id', 'dept_name', 'description']
    ordering_fields = ['dept_id', 'dept_name', 'created_at']

    @action(detail=True)
    def employees(self, request, dept_id=None):
        """Get all employees for a department"""
        department = self.get_object()
        employees = department.employees.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class AccessLevelViewSet(viewsets.ModelViewSet):
    """
    API endpoint for AccessLevel CRUD operations.
    """
    queryset = AccessLevel.objects.all()
    serializer_class = AccessLevelSerializer
    lookup_field = 'access_id'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AccessLevelFilter
    search_fields = ['access_id', 'access_name', 'description']
    ordering_fields = ['access_id', 'access_name', 'risk_score', 'created_at']

    @action(detail=True)
    def employees(self, request, access_id=None):
        """Get all employees with this access level"""
        access_level = self.get_object()
        employees = access_level.employees.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Employee CRUD operations.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'employee_id'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EmployeeFilter
    search_fields = ['employee_id', 'first_name', 'last_name', 'email', 'job_title']
    ordering_fields = ['employee_id', 'last_name', 'first_name', 'hire_date', 'created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmployeeDetailSerializer
        return self.serializer_class

    @action(detail=True, methods=['get'])
    def access_levels(self, request, employee_id=None):
        """Get all access levels for an employee"""
        employee = self.get_object()
        serializer = EmployeeAccessSerializer(
            employee.employeeaccess_set.all(), many=True
        )
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def audit_logs(self, request, employee_id=None):
        """Get audit logs for an employee"""
        employee = self.get_object()
        serializer = AccessAuditLogSerializer(
            employee.audit_logs.all(), many=True
        )
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def grant_access(self, request, employee_id=None):
        """Grant an access level to an employee"""
        employee = self.get_object()
        
        # Validate input
        if not request.data.get('access_level'):
            return Response(
                {"error": "access_level is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        access_level_id = request.data.get('access_level')
        try:
            access_level = AccessLevel.objects.get(access_id=access_level_id)
        except AccessLevel.DoesNotExist:
            return Response(
                {"error": f"Access level with ID {access_level_id} does not exist"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if access already exists
        employee_access, created = EmployeeAccess.objects.get_or_create(
            employee=employee,
            access_level=access_level,
            defaults={
                'granted_by': request.data.get('granted_by', request.user.username if hasattr(request, 'user') else 'API'),
                'notes': request.data.get('notes', '')
            }
        )
        
        if not created:
            # If access exists but was revoked, reactivate it
            if not employee_access.is_active:
                employee_access.is_active = True
                employee_access.revoked_date = None
                employee_access.revoked_by = None
                employee_access.save()
            else:
                return Response(
                    {"message": f"Employee already has {access_level.access_name} access"}, 
                    status=status.HTTP_200_OK
                )
        
        # Create audit log
        AccessAuditLog.objects.create(
            employee=employee,
            access_level=access_level,
            action='granted',
            action_by=request.data.get('granted_by', request.user.username if hasattr(request, 'user') else 'API'),
            notes=request.data.get('notes', '')
        )
        
        serializer = EmployeeAccessSerializer(employee_access)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def revoke_access(self, request, employee_id=None):
        """Revoke an access level from an employee"""
        employee = self.get_object()
        
        # Validate input
        if not request.data.get('access_level'):
            return Response(
                {"error": "access_level is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        access_level_id = request.data.get('access_level')
        
        try:
            employee_access = EmployeeAccess.objects.get(
                employee=employee,
                access_level__access_id=access_level_id,
                is_active=True
            )
        except EmployeeAccess.DoesNotExist:
            return Response(
                {"error": f"Employee does not have active access to {access_level_id}"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Revoke access
        employee_access.is_active = False
        employee_access.revoked_date = request.data.get('revoked_date')
        employee_access.revoked_by = request.data.get('revoked_by', request.user.username if hasattr(request, 'user') else 'API')
        employee_access.save()
        
        # Create audit log
        AccessAuditLog.objects.create(
            employee=employee,
            access_level=employee_access.access_level,
            action='revoked',
            action_by=employee_access.revoked_by,
            notes=request.data.get('notes', '')
        )
        
        serializer = EmployeeAccessSerializer(employee_access)
        return Response(serializer.data)


class EmployeeAccessViewSet(viewsets.ModelViewSet):
    """
    API endpoint for EmployeeAccess CRUD operations.
    """
    queryset = EmployeeAccess.objects.all()
    serializer_class = EmployeeAccessSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EmployeeAccessFilter
    search_fields = ['employee__first_name', 'employee__last_name', 'access_level__access_name']
    ordering_fields = ['granted_date', 'revoked_date']


class AccessAuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for AccessAuditLog (read-only).
    """
    queryset = AccessAuditLog.objects.all()
    serializer_class = AccessAuditLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AccessAuditLogFilter
    search_fields = ['employee__first_name', 'employee__last_name', 'access_level__access_name', 'action_by']
    ordering_fields = ['action_date']