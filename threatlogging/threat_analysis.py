import requests
import json
from .models import Threat

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
GEMINI_API_KEY = "AIzaSyBywvuqS6Qoiag4O4V_TQseZ0MR72aPGfI"

def generate_threat_prompt(log_type, log_data):
    """
    Create a detailed threat detection prompt for Gemini.
    """
    return f""" 
    You are a cybersecurity threat detection assistant. Analyze the following log entry of type '{log_type}' and determine if it indicates a potential security threat.

    Log Entry: {log_data}

    Respond in the following JSON format:
    {{
      "is_threat": true/false,
      "risk_score": float between 0 and 1,
      "description": "A short explanation of the threat or why it's safe."
    }}
    """

def process_log_entry(log_instance, log_type):
    """
    Uses Gemini to analyze a log and optionally create a Threat.
    """
    # Create base data dictionary with non-None values only
    data = {k: v for k, v in {
        "username": getattr(log_instance, "username", None),
        "department": getattr(log_instance, "department", None),
        "message": getattr(log_instance, "message", None),
        "timestamp": str(getattr(log_instance, "timestamp", "")),
        "system": getattr(log_instance, "system", None),
    }.items() if v is not None}
    
    print(data)
    
    # Add log-type-specific fields, filtering out None values
    if log_type == "Access":
        data.update({k: v for k, v in {
            "action": getattr(log_instance, 'action', None),
            "ip_address": getattr(log_instance, 'ip_address', None),
            "device": getattr(log_instance, 'device', None),
            "location": getattr(log_instance, 'location', None),
        }.items() if v is not None})
    elif log_type == "Activity":
        data.update({k: v for k, v in {
            "resource": getattr(log_instance, 'resource', None),
            "action": getattr(log_instance, 'action', None),
            "status": getattr(log_instance, 'status', None),
            "justification": getattr(log_instance, 'justification', None),
        }.items() if v is not None})
    elif log_type == "Error":
        data.update({k: v for k, v in {
            "error_type": getattr(log_instance, 'error_type', None),
            "severity": getattr(log_instance, 'severity', None),
            "originating_module": getattr(log_instance, 'originating_module', None),
        }.items() if v is not None})
    
    prompt = generate_threat_prompt(log_type, data)
    
    try:
        # Make request to Gemini API
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {"parts": [{"text": prompt}]}
                ]
            },
            timeout=10
        )
        
        # Check if response is successful
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        print(result)
        # Check if response contains expected structure
        if 'candidates' not in result or not result['candidates']:
            print(f"[Threat Detection] Unexpected API response format: {result}")
            return
            
        # Extract text from response
        gemini_reply = result['candidates'][0]['content']['parts'][0]['text']
        
        # Clean up response text to ensure valid JSON
        # Find JSON in the response (in case there's extra text)
        import re
        json_match = re.search(r'\{[\s\S]*\}', gemini_reply)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = gemini_reply
            
        # Parse Gemini reply
        try:
            parsed = json.loads(json_str)
            
            if parsed.get("is_threat"):
                # Check if we're using the old schema or new schema
                from django.db import connection
                cursor = connection.cursor()
                cursor.execute("PRAGMA table_info(threatlogging_threat)")
                columns = [column[1] for column in cursor.fetchall()]
                
                threat_data = {
                    "log_type": log_type,
                    "description": parsed.get("description", "Possible threat detected."),
                    "risk_score": parsed.get("risk_score", 0.5)
                }
                
                # If the content_type field exists, use the ContentType framework
                if 'content_type_id' in columns:
                    from django.contrib.contenttypes.models import ContentType
                    threat_data.update({
                        "content_type": ContentType.objects.get_for_model(log_instance),
                        "object_id": log_instance.id
                    })
                # Otherwise, use the old log_id field if it exists
                elif 'log_id' in columns:
                    threat_data["log_id"] = log_instance.id
                
                Threat.objects.create(**threat_data)
                
        except json.JSONDecodeError as json_err:
            print(f"[Threat Detection] JSON parsing error: {json_err}")
            print(f"Raw response: {gemini_reply}")
            
    except requests.exceptions.RequestException as req_err:
        print(f"[Threat Detection] API request error: {req_err}")
    except Exception as e:
        print(f"[Threat Detection] Unexpected error: {e}")
        # Log more details for debugging
        import traceback
        traceback.print_exc()