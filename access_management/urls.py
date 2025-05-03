from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'departments', views.DepartmentViewSet, basename='department')
router.register(r'access-levels', views.AccessLevelViewSet, basename='access-level')
router.register(r'employees', views.EmployeeViewSet, basename='employee')
router.register(r'employee-access', views.EmployeeAccessViewSet, basename='employee-access')
router.register(r'audit-logs', views.AccessAuditLogViewSet, basename='audit-log')

app_name = 'access_management'

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]