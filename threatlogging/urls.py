from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccessLogViewSet, ActivityLogViewSet, ErrorLogViewSet, ThreatViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'access', AccessLogViewSet)
router.register(r'activity', ActivityLogViewSet)
router.register(r'error', ErrorLogViewSet)
router.register(r"threat", ThreatViewSet)
app_name = 'threatlogging'

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]