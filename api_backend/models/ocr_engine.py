import pytesseract
from PIL import Image
import re

# ⚠️ path set करो (IMPORTANT)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class OCREngine:

    def extract_text(self, image_path):
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)

            return text.lower()

        except Exception as e:
            return f"error: {str(e)}"

    def detect_phishing(self, text):
        score = 0
        reasons = []

        keywords = [
            "verify", "login", "bank", "account", "update",
            "password", "urgent", "click", "confirm", "security"
        ]

        for k in keywords:
            if k in text:
                score += 10
                reasons.append(f"Keyword: {k}")

        urls = re.findall(r'https?://\S+', text)
        if urls:
            score += 20
            reasons.append("URL detected in image")

        if score > 40:
            status = "PHISHING"
        elif score > 20:
            status = "SUSPICIOUS"
        else:
            status = "SAFE"

        return {
            "status": status,
            "score": score,
            "reasons": reasons
        }