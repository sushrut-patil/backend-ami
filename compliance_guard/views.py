from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse

from .models import Compliance
from .serializers import ComplianceSerializer


class ComplianceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Compliance CRUD operations.
    """
    queryset = Compliance.objects.all().order_by('-created_at')
    serializer_class = ComplianceSerializer
    # No permission_classes or authentication_classes
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['title', 'description', 'requirements', 'notes']
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'category', 'status']

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get compliances filtered by category"""
        category = request.query_params.get('category', None)
        if category:
            compliances = Compliance.objects.filter(category=category).order_by('-created_at')
            serializer = self.get_serializer(compliances, many=True)
            return Response(serializer.data)
        return Response({"error": "Category parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Get compliances filtered by status"""
        status_param = request.query_params.get('status', None)
        if status_param:
            compliances = Compliance.objects.filter(status=status_param).order_by('-created_at')
            serializer = self.get_serializer(compliances, many=True)
            return Response(serializer.data)
        return Response({"error": "Status parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Change the status of a compliance"""
        compliance = self.get_object()
        new_status = request.data.get('status', None)
        
        if new_status and new_status in dict(Compliance.STATUS_CHOICES).keys():
            compliance.status = new_status
            compliance.save()
            serializer = self.get_serializer(compliance)
            return Response(serializer.data)
        return Response({"error": "Valid status parameter is required"}, status=status.HTTP_400_BAD_REQUEST)


class SecurityChatbotView(APIView):
    """
    API view for the security chatbot using Google's Gemini API
    """
    def post(self, request, *args, **kwargs):
        """Handle POST requests to interact with the chatbot"""
        # Get the query from the request
        query = request.data.get('query', '')
        if not query:
            return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Configure the Gemini API with settings from environment
            if not hasattr(settings, 'GEMINI_API_KEY') or not settings.GEMINI_API_KEY:
                return Response(
                    {"error": "Gemini API key is not configured"}, 
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
                
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # Define a security context to help the model understand it should focus on security
            security_context = """
            You are a cybersecurity and compliance expert assistant for a security application.
            Provide accurate, helpful information about security best practices, compliance requirements,
            and security threats. Focus on actionable advice and cite relevant standards or regulations when applicable.
            Do not provide information about how to exploit vulnerabilities or bypass security measures.
            """
            
            # Prepare the prompt with context
            full_prompt = f"{security_context}\n\nUser question: {query}"
            
            # Get a response from Gemini
            model = genai.GenerativeModel('gemini-1.5-flash-8b')
            response = model.generate_content(full_prompt)
            
            # Return the response
            return Response({
                "query": query,
                "response": response.text
            })
        
        except Exception as e:
            # Log the error
            print(f"Error in security_chatbot: {str(e)}")
            return Response(
                {"error": "Failed to get a response from the AI model", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExplainComplianceView(APIView):
    """
    API view to explain compliance requirements based on the selected category
    """
    def get(self, request, *args, **kwargs):
        """Handle GET requests for compliance explanations"""
        # Get the compliance category from the request
        category = request.query_params.get('category', '')
        if not category:
            return Response({"error": "Category parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Check if the required API key is set
            if not hasattr(settings, 'GEMINI_API_KEY') or not settings.GEMINI_API_KEY:
                return Response(
                    {"error": "Gemini API key is not configured"}, 
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            # Configure the Gemini API
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # Map category to its full name for better context
            category_map = dict(Compliance.CATEGORY_CHOICES)
            full_category_name = category_map.get(category, category)
            
            # Define the prompt to explain the compliance category
            prompt = f"""
            As a compliance expert, provide a detailed explanation of {full_category_name} ({category}).
            Include the following information:
            
            1. Overview and purpose of the compliance standard
            2. Key requirements and controls
            3. Who needs to comply with this standard
            4. Penalties or consequences for non-compliance
            5. Best practices for achieving and maintaining compliance
            6. Common challenges organizations face with this compliance standard
            
            Keep the explanation thorough but accessible for security professionals.
            """
            
            # Get a response from Gemini
            model = genai.GenerativeModel('gemini-1.5-flash-8b')
            response = model.generate_content(prompt)
            
            # Return the response
            return Response({
                "category": category,
                "full_name": full_category_name,
                "explanation": response.text
            })
        
        except Exception as e:
            print(f"Error in explain_compliance: {str(e)}")
            return Response(
                {"error": "Failed to get compliance explanation", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )