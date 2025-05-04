from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'compliance', views.ComplianceViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('chatbot/', views.SecurityChatbotView.as_view(), name='security-chatbot'),
    path('explain-compliance/', views.ExplainComplianceView.as_view(), name='explain-compliance'),
]