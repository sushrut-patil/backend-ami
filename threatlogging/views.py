from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.contenttypes.models import ContentType
from .models import AccessLog, ActivityLog, ErrorLog, Threat
from .serializers import AccessLogSerializer, ActivityLogSerializer, ErrorLogSerializer, ThreatSerializer


class AccessLogViewSet(viewsets.GenericViewSet,
                         viewsets.mixins.CreateModelMixin,
                         viewsets.mixins.ListModelMixin,
                         viewsets.mixins.RetrieveModelMixin):
    """
    API endpoint for AccessLog CRUD operations.
    """
    queryset = AccessLog.objects.all().order_by('-timestamp')
    serializer_class = AccessLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['username', 'department', 'action', 'access_level', 'system']
    search_fields = ['username', 'department', 'message', 'action', 'ip_address', 'device', 'location']
    ordering_fields = ['timestamp', 'username', 'department', 'action']

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_user(self, request):
        """Get all access logs for a specific user"""
        username = request.query_params.get('username', None)
        if username:
            logs = AccessLog.objects.filter(username=username).order_by('-timestamp')
            serializer = self.get_serializer(logs, many=True)
            return Response(serializer.data)
        return Response({"error": "Username parameter is required"}, status=400)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_department(self, request):
        """Get all access logs for a specific department"""
        department = request.query_params.get('department', None)
        if department:
            logs = AccessLog.objects.filter(department=department).order_by('-timestamp')
            serializer = self.get_serializer(logs, many=True)
            return Response(serializer.data)
        return Response({"error": "Department parameter is required"}, status=400)


class ActivityLogViewSet(viewsets.GenericViewSet,
                           viewsets.mixins.CreateModelMixin,
                           viewsets.mixins.ListModelMixin,
                           viewsets.mixins.RetrieveModelMixin):
    """
    API endpoint for ActivityLog CRUD operations.
    """
    queryset = ActivityLog.objects.all().order_by('-timestamp')
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['username', 'department', 'resource', 'action', 'status', 'system']
    search_fields = ['username', 'department', 'message', 'resource', 'action', 'justification']
    ordering_fields = ['timestamp', 'username', 'department', 'resource', 'action', 'status']

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_resource(self, request):
        """Get all activity logs for a specific resource"""
        resource = request.query_params.get('resource', None)
        if resource:
            logs = ActivityLog.objects.filter(resource=resource).order_by('-timestamp')
            serializer = self.get_serializer(logs, many=True)
            return Response(serializer.data)
        return Response({"error": "Resource parameter is required"}, status=400)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_status(self, request):
        """Get all activity logs with a specific status"""
        status = request.query_params.get('status', None)
        if status:
            logs = ActivityLog.objects.filter(status=status).order_by('-timestamp')
            serializer = self.get_serializer(logs, many=True)
            return Response(serializer.data)
        return Response({"error": "Status parameter is required"}, status=400)


class ErrorLogViewSet(viewsets.GenericViewSet,
                        viewsets.mixins.CreateModelMixin,
                        viewsets.mixins.ListModelMixin,
                        viewsets.mixins.RetrieveModelMixin):
    """
    API endpoint for ErrorLog CRUD operations.
    """
    queryset = ErrorLog.objects.all().order_by('-timestamp')
    serializer_class = ErrorLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['username', 'department', 'error_type', 'severity', 'originating_module', 'system']
    search_fields = ['username', 'department', 'message', 'error_type', 'stack_trace', 'originating_module']
    ordering_fields = ['timestamp', 'username', 'department', 'error_type', 'severity']

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_severity(self, request):
        """Get all error logs with a specific severity level"""
        severity = request.query_params.get('severity', None)
        if severity:
            logs = ErrorLog.objects.filter(severity=severity).order_by('-timestamp')
            serializer = self.get_serializer(logs, many=True)
            return Response(serializer.data)
        return Response({"error": "Severity parameter is required"}, status=400)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_error_type(self, request):
        """Get all error logs of a specific error type"""
        error_type = request.query_params.get('error_type', None)
        if error_type:
            logs = ErrorLog.objects.filter(error_type=error_type).order_by('-timestamp')
            serializer = self.get_serializer(logs, many=True)
            return Response(serializer.data)
        return Response({"error": "Error type parameter is required"}, status=400)


class ThreatViewSet(viewsets.GenericViewSet,
                    viewsets.mixins.ListModelMixin,
                    viewsets.mixins.RetrieveModelMixin,
                    viewsets.mixins.UpdateModelMixin,
                    viewsets.mixins.CreateModelMixin):
    """
    API endpoint for Threat CRUD operations.
    """
    queryset = Threat.objects.all().order_by('-detected_at')
    serializer_class = ThreatSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['log_type', 'status', 'escalated']
    search_fields = ['description']
    ordering_fields = ['detected_at', 'risk_score', 'status']

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_log_type(self, request):
        """Get all threats for a specific log type"""
        log_type = request.query_params.get('log_type', None)
        if log_type:
            threats = Threat.objects.filter(log_type=log_type).order_by('-detected_at')
            serializer = self.get_serializer(threats, many=True)
            return Response(serializer.data)
        return Response({"error": "Log type parameter is required"}, status=400)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_status(self, request):
        """Get all threats with a specific status"""
        status = request.query_params.get('status', None)
        if status:
            threats = Threat.objects.filter(status=status).order_by('-detected_at')
            serializer = self.get_serializer(threats, many=True)
            return Response(serializer.data)
        return Response({"error": "Status parameter is required"}, status=400)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def resolve(self, request, pk=None):
        """Mark a threat as resolved"""
        threat = self.get_object()
        username = request.data.get('resolved_by', request.user.username)
        
        threat.status = 'Resolved'
        threat.resolved_by = username
        threat.resolved_at = timezone.now()
        threat.save()
        
        serializer = self.get_serializer(threat)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def escalate(self, request, pk=None):
        """Escalate a threat"""
        threat = self.get_object()
        
        threat.status = 'Escalated'
        threat.escalated = True
        threat.save()
        
        serializer = self.get_serializer(threat)
        return Response(serializer.data)