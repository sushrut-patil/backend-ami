import requests
from .models import Threat

# TODO: Replace with your real Gemini Pro API endpoint/key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
GEMINI_API_KEY = "AIzaSyBywvuqS6Qoiag4O4V_TQseZ0MR72aPGfI"

def generate_threat_prompt(log_type, log_data):
    """
    Create a detailed threat detection prompt for Gemini.
    """
    return f"""
You are a cybersecurity threat detection assistant.
Analyze the following log entry of type '{log_type}' and determine if it indicates a potential security threat.

Log Entry:
{log_data}

Respond in the following JSON format:
{{
  "is_threat": true/false,
  "risk_score": float between 0 and 1,
  "description": "A short explanation of the threat or why it's safe."
}}
"""

def analyze_log_entry(log_instance, log_type):
    """
    Uses Gemini to analyze a log and optionally create a Threat.
    """
    data = {
        "username": log_instance.username,
        "department": log_instance.department,
        "message": log_instance.message,
        "timestamp": str(log_instance.timestamp),
        "system": log_instance.system,
    }

    # Add log-type-specific fields
    if log_type == "Access":
        data.update({
            "action": getattr(log_instance, 'action', None),
            "ip_address": getattr(log_instance, 'ip_address', None),
            "device": getattr(log_instance, 'device', None),
            "location": getattr(log_instance, 'location', None),
        })
    elif log_type == "Activity":
        data.update({
            "resource": getattr(log_instance, 'resource', None),
            "action": getattr(log_instance, 'action', None),
            "status": getattr(log_instance, 'status', None),
            "justification": getattr(log_instance, 'justification', None),
        })
    elif log_type == "Error":
        data.update({
            "error_type": getattr(log_instance, 'error_type', None),
            "severity": getattr(log_instance, 'severity', None),
            "originating_module": getattr(log_instance, 'originating_module', None),
        })

    prompt = generate_threat_prompt(log_type, data)

    try:
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
        result = response.json()
        gemini_reply = result['candidates'][0]['content']['parts'][0]['text']

        # Parse Gemini reply
        import json
        parsed = json.loads(gemini_reply)

        if parsed.get("is_threat"):
            Threat.objects.create(
                log_type=log_type,
                log_id=log_instance.id,
                description=parsed.get("description", "Possible threat detected."),
                risk_score=parsed.get("risk_score", 0.5)
            )
    except Exception as e:
        print(f"[Threat Detection] Gemini API error: {e}")
