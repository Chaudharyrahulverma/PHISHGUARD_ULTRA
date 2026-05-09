import pytesseract
from PIL import Image
import re

from models.content_detector import analyze_content

# 👉 अगर Windows है तो path set करो
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# 🔗 Extract URLs from text
def extract_urls(text):
    return re.findall(r'(https?://[^\s]+)', text)


# 🔍 OCR + Smart Detection
def scan_image(file):

    try:
        # 📸 Load image
        image = Image.open(file)

        # 🔠 OCR text extraction
        extracted_text = pytesseract.image_to_string(image)

        if not extracted_text.strip():
            return {
                "verdict": "UNKNOWN",
                "confidence": "LOW",
                "message": "No readable text found"
            }

        # 🔍 Analyze content
        result = analyze_content(extracted_text)

        # 🔗 Extract links
        urls = extract_urls(extracted_text)

        # 🧠 Improve result using links
        if urls:
            result["reasons"].append(f"{len(urls)} URL(s) found in image")

        return {
            "verdict": result["verdict"],
            "score": result["score"],
            "confidence": result["confidence"],
            "reasons": result["reasons"],
            "extracted_text": extracted_text[:500],  # limit
            "urls_found": urls
        }

    except Exception as e:
        return {
            "verdict": "ERROR",
            "confidence": "LOW",
            "message": str(e)
        }