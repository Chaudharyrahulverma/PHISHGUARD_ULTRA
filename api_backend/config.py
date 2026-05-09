# ========================================
# PHISHGUARD ULTRA - CONFIGURATION
# ========================================

import os
from dotenv import load_dotenv

# Load environment variables from .env file (if exists)
load_dotenv()

# ========================================
# API KEYS (Future Ready - No Key Required Now)
# ========================================
# Note: Gemini/OpenAI keys are OPTIONAL. AI works without them.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", None)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

# ========================================
# SECURITY SETTINGS
# ========================================
# API Key for backend authentication (optional - disable if not needed)
API_KEY = os.getenv("API_KEY", "phishguard-ultra-2024")

# Enable/Disable API Key check (False = no authentication needed)
REQUIRE_API_KEY = False

# ========================================
# RATE LIMITING
# ========================================
# Maximum requests per minute per IP
RATE_LIMIT = "30 per minute"

# ========================================
# FILE UPLOAD SETTINGS
# ========================================
# Max file size (5 MB)
MAX_FILE_SIZE = 5 * 1024 * 1024

# Allowed file types for image upload
ALLOWED_IMAGE_TYPES = ["image/png", "image/jpeg", "image/jpg", "image/webp"]

# ========================================
# DATABASE SETTINGS
# ========================================
DATABASE_PATH = "database/db.sqlite3"
LOG_DATABASE_PATH = "database/logs.db"

# ========================================
# CORS SETTINGS
# ========================================
# Allowed origins for frontend
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5000",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "*"  # Allow all (change in production)
]

# ========================================
# LOGGING SETTINGS
# ========================================
LOG_LEVEL = "INFO"
LOG_FILE = "logs/app.log"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# ========================================
# AI SETTINGS
# ========================================
# AI Memory settings
MAX_MEMORY_MESSAGES = 10  # Store last 10 messages per user

# Follow-up detection keywords
FOLLOWUP_KEYWORDS = ["more", "detail", "again", "explain", "next", "tell me more"]

# ========================================
# SCANNER SETTINGS
# ========================================
# URL Scanner
RISKY_TLDS = ["tk", "ml", "ga", "cf", "xyz", "top", "click", "download"]
SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "update", "bank",
    "account", "free", "gift", "bonus", "urgent",
    "confirm", "signin", "reset", "password", "verify"
]
BRANDS = [
    "paypal", "google", "facebook", "amazon",
    "microsoft", "apple", "netflix", "instagram",
    "sbi", "hdfc", "icici", "axis", "flipkart", "amazon"
]

# Password Scanner
COMMON_PASSWORDS = [
    "123456", "password", "qwerty", "admin", "welcome",
    "12345678", "abc123", "password123", "admin123"
]

# Email Scanner
DISPOSABLE_DOMAINS = [
    "tempmail", "10minutemail", "mailinator", "guerrillamail",
    "trashmail", "yopmail", "throwaway", "temp-mail"
]

# ========================================
# TESSERACT PATH (Cross-platform)
# ========================================
import platform

if platform.system() == "Windows":
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
elif platform.system() == "Darwin":  # macOS
    TESSERACT_PATH = "/usr/local/bin/tesseract"
else:  # Linux
    TESSERACT_PATH = "/usr/bin/tesseract"

# ========================================
# HELPER FUNCTION
# ========================================
def get_config():
    """Return all config as dictionary"""
    return {
        "api_key_required": REQUIRE_API_KEY,
        "rate_limit": RATE_LIMIT,
        "max_file_size": MAX_FILE_SIZE,
        "allowed_image_types": ALLOWED_IMAGE_TYPES,
        "cors_origins": ALLOWED_ORIGINS,
        "log_level": LOG_LEVEL
    }