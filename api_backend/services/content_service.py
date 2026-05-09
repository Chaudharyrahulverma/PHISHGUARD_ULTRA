# services/content_service.py

from models.content_detector import analyze_content

# 🚀 Init (optional - future ML / dataset load)
def init():
    print("📄 Content Detection Service Ready")

# 🔍 Scan function (IMPORTANT: receives STRING directly)
def scan(text):

    # Safety check
    if not text or not isinstance(text, str):
        return {
            "verdict": "ERROR",
            "score": 0,
            "confidence": "LOW",
            "reasons": ["Invalid input"]
        }

    # Call model
    result = analyze_content(text)

    return result