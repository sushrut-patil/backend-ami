from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@require_http_methods(["GET"])
def get_threat_data(request):
    """
    View to provide threat path analysis data
    """
    # In a real application, this data might come from a database
    threat_data = {
        "nodes": [
            { 
                "id": "n1", 
                "label": "Kajal Prajapati Views Records", 
                "type": "action",
                "system": "HRMS",
                "resource": "Employee Records",
                "user": "Kajal Prajapati",
                "department": "HRMIS",
                "accessLevel": "User",
                "timestamp": "2025-04-28 14:23:41",
                "status": "Success",
                "suspiciousLevel": "low",
                "description": "Viewing employee records is within normal permissions, but could be part of reconnaissance if followed by other actions."
            },
            { 
                "id": "n2", 
                "label": "Chetan Rana Deletion Attempt", 
                "type": "action",
                "system": "CRM",
                "resource": "Budget Sheet",
                "user": "Chetan Rana",
                "department": "Projects",
                "accessLevel": "Admin",
                "timestamp": "2025-04-30 09:10:25",
                "status": "Failed",
                "suspiciousLevel": "high",
                "description": "Failed deletion attempt of budget data by admin user could indicate malicious intent or system protection mechanisms working correctly."
            },
            { 
                "id": "n3", 
                "label": "Amar Gupta Downloads Directory", 
                "type": "action",
                "system": "Inventory",
                "resource": "User Directory",
                "user": "Amar Gupta",
                "department": "Market Research",
                "accessLevel": "Manager",
                "timestamp": "2025-05-01 17:55:12",
                "status": "Success",
                "suspiciousLevel": "medium",
                "description": "Downloading a user directory from Inventory system by a Market Research manager could represent data exfiltration."
            },
            { 
                "id": "n4", 
                "label": "Employee Records", 
                "type": "resource",
                "system": "HRMS",
                "criticality": "high",
                "description": "Contains sensitive personal information about employees."
            },
            { 
                "id": "n5", 
                "label": "Budget Sheet", 
                "type": "resource",
                "system": "CRM",
                "criticality": "high",
                "description": "Contains financial planning information and sensitive business data."
            },
            { 
                "id": "n6", 
                "label": "User Directory", 
                "type": "resource",
                "system": "Inventory",
                "criticality": "medium",
                "description": "Contains user contact information and potentially system access details."
            },
            { 
                "id": "n7", 
                "label": "HRMS System", 
                "type": "system",
                "criticality": "high",
                "description": "Human Resources Management System containing employee data."
            },
            { 
                "id": "n8", 
                "label": "CRM System", 
                "type": "system",
                "criticality": "high",
                "description": "Customer Relationship Management system with financial data."
            },
            { 
                "id": "n9", 
                "label": "Inventory System", 
                "type": "system",
                "criticality": "medium",
                "description": "Inventory tracking system with product and user information."
            }
        ],
        "edges": [
            # Path 1: Potential data reconnaissance and exfiltration
            { "id": "e1", "source": "n1", "target": "n4", "label": "accesses", "pathId": "path1" },
            { "id": "e2", "source": "n4", "target": "n3", "label": "leads to", "pathId": "path1" },
            { "id": "e3", "source": "n3", "target": "n6", "label": "extracts", "pathId": "path1" },
            
            # Path 2: Failed deletion attempt
            { "id": "e4", "source": "n2", "target": "n5", "label": "attempts to delete", "pathId": "path2" },
            { "id": "e5", "source": "n5", "target": "n8", "label": "contained in", "pathId": "path2" },
            
            # Path 3: Cross-system activity
            { "id": "e6", "source": "n1", "target": "n7", "label": "operates on", "pathId": "path3" },
            { "id": "e7", "source": "n7", "target": "n9", "label": "shares data with", "pathId": "path3" },
            { "id": "e8", "source": "n9", "target": "n3", "label": "enables", "pathId": "path3" },
            
            # Resource to system relationships
            { "id": "e9", "source": "n4", "target": "n7", "label": "belongs to", "pathId": None },
            { "id": "e10", "source": "n5", "target": "n8", "label": "belongs to", "pathId": None },
            { "id": "e11", "source": "n6", "target": "n9", "label": "belongs to", "pathId": None }
        ],
        "paths": [
            {
                "id": "path1",
                "name": "Data Reconnaissance and Exfiltration",
                "description": "This path shows a potential data breach where an employee first accesses HR records (possibly for reconnaissance) followed by a different user downloading user directory data (possible exfiltration).",
                "severity": 8,
                "entryPoint": "n1",
                "criticalResources": ["Employee Records", "User Directory"],
                "riskFactors": ["Cross-department access", "Data exfiltration", "Multiple systems involved"],
                "recommendation": "Implement stricter controls on user directory downloads and monitor patterns of record access followed by downloads."
            },
            {
                "id": "path2",
                "name": "Failed Financial Data Deletion",
                "description": "An admin user attempted to delete budget sheets but failed. Though the justification states 'duplication cleanup', this could represent an attempted data destruction attack.",
                "severity": 7,
                "entryPoint": "n2",
                "criticalResources": ["Budget Sheet"],
                "riskFactors": ["Admin privileges", "Data destruction attempt", "Failed operation"],
                "recommendation": "Review admin deletion privileges and implement approval workflows for sensitive financial data deletion."
            },
            {
                "id": "path3",
                "name": "Cross-System Data Access Chain",
                "description": "This path demonstrates how a user viewing HR records may be connected to another user downloading data from the Inventory system, possibly through shared data between systems.",
                "severity": 6,
                "entryPoint": "n1",
                "criticalResources": ["Employee Records", "User Directory"],
                "riskFactors": ["Cross-system data flow", "Multiple departments", "Data extraction"],
                "recommendation": "Audit data sharing between HRMS and Inventory systems, implement tighter controls on cross-system data access."
            }
        ]
    }
    
    return JsonResponse(threat_data)

# Optional: If you want more dynamic data, you could add methods to filter or modify the data
@csrf_exempt
@require_http_methods(["GET"])
def get_threat_path(request, path_id):
    """
    View to provide a specific threat path
    """
    # Get the data
    threat_data = get_full_threat_data()
    
    # Filter to just the requested path
    path = next((p for p in threat_data["paths"] if p["id"] == path_id), None)
    
    if not path:
        return JsonResponse({"error": "Path not found"}, status=404)
    
    # Get nodes and edges associated with this path
    edges = [e for e in threat_data["edges"] if e["pathId"] == path_id]
    
    # Get all node IDs referenced in these edges
    node_ids = set()
    for edge in edges:
        node_ids.add(edge["source"])
        node_ids.add(edge["target"])
    
    # Filter to just these nodes
    nodes = [n for n in threat_data["nodes"] if n["id"] in node_ids]
    
    result = {
        "path": path,
        "nodes": nodes,
        "edges": edges
    }
    
    return JsonResponse(result)

# Helper function to get the full dataset
def get_full_threat_data():
    """
    This would typically access a database or other data source
    For this example, we'll hardcode the data
    """
    # Return same data as in get_threat_data
    # In a real application, you might fetch this from a model/database
    # ...
    
# Add this to your urls.py
# path('api/threat-data/', views.get_threat_data, name='get_threat_data'),
# path('api/threat-path/<str:path_id>/', views.get_threat_path, name='get_threat_path'),