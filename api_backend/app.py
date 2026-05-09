# ========================================
# PHISHGUARD ULTRA - MAIN APP (STRONG VERSION)
# Security + Logging + Validation Added
# ========================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import re
import os

# ================= CONFIG =================
from config import (
    RATE_LIMIT,
    MAX_FILE_SIZE,
    ALLOWED_IMAGE_TYPES,
    REQUIRE_API_KEY,
    API_KEY,
    ALLOWED_ORIGINS
)

# ================= SERVICES =================
from services.url_service import init as url_init, scan as url_scan
from services.email_service import init as email_init, scan as email_scan
from services.content_service import init as content_init, scan as content_scan
from services.image_service import scan_image
from services.ai_brain import process_message

# ================= SAFETY & LOGGING =================
from services.safety_service import (
    validate_url, validate_email_address, validate_content,
    validate_password, validate_image_file, sanitize_input
)
from services.logging_service import (
    log_api_request, log_error, log_scan_history, log_info,
    app_logger
)

# ================= DB =================
from database.db_handler import (
    init_db,
    save_url_scan,
    save_email_scan,
    create_report_table
)

# ================= INIT APP =================
app = Flask(__name__)

# CORS Configuration
CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGINS}})

print("🔥 PhishGuard Ultra Server Starting...")
app_logger.info("🚀 Application Starting")

# ================= INIT DATABASES =================
init_db()
create_report_table()

# ================= LOAD DATASETS =================
def load_file(path):
    data = set()
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data.add(line)
        else:
            print(f"⚠️ File not found: {path}")
    except Exception as e:
        print(f"❌ Failed loading {path}: {e}")
    return data

print("📂 Loading datasets...")

# Try multiple possible paths for datasets
dataset_paths = [
    "models/dataset/clean_urls.txt",
    "../ml_model/dataset/clean_urls.txt",
    "ml_model/dataset/clean_urls.txt"
]

urls = set()
emails = set()

for path in dataset_paths:
    if os.path.exists(path):
        urls = load_file(path)
        break

email_paths = [
    "models/dataset/clean_emails.txt",
    "../ml_model/dataset/clean_emails.txt",
    "ml_model/dataset/clean_emails.txt"
]

for path in email_paths:
    if os.path.exists(path):
        emails = load_file(path)
        break

url_init(urls)
email_init(emails)
content_init()

print(f"✅ Data Loaded - URLs: {len(urls)}, Emails: {len(emails)}")
app_logger.info(f"Data loaded - URLs: {len(urls)}, Emails: {len(emails)}")

# ================= MIDDLEWARE: API KEY CHECK =================
def check_api_key():
    """Optional API key validation"""
    if not REQUIRE_API_KEY:
        return True
    
    api_key = request.headers.get('X-API-Key')
    if not api_key or api_key != API_KEY:
        return False
    return True

# ================= MIDDLEWARE: REQUEST LOGGING =================
@app.before_request
def before_request():
    """Log request start time"""
    request.start_time = time.time()

@app.after_request
def after_request(response):
    """Log request after completion"""
    if hasattr(request, 'start_time'):
        response_time = (time.time() - request.start_time) * 1000  # milliseconds
        
        # Log to database
        log_api_request(
            endpoint=request.endpoint or request.path,
            method=request.method,
            ip_address=request.remote_addr,
            status_code=response.status_code,
            response_time=round(response_time, 2)
        )
        
        # Log to file
        app_logger.info(f"{request.method} {request.path} - {response.status_code} - {response_time:.2f}ms")
    
    return response

# ================= HOME =================
@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "name": "PhishGuard Ultra",
        "version": "2.0.0",
        "message": "🚀 Backend is running strong!",
        "endpoints": [
            "/check-url", "/check-email", "/check-content",
            "/check-password", "/check-image", "/chat", "/submit-report"
        ]
    })

# ================= URL SCAN (WITH VALIDATION) =================
@app.route("/check-url", methods=["POST"])
def check_url():
    try:
        # API Key check
        if not check_api_key():
            return jsonify({"error": "Invalid API Key"}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        url = data.get("url", "")
        
        # Validate URL
        is_valid, sanitized_url, error_msg = validate_url(url)
        if not is_valid:
            return jsonify({"error": error_msg, "status": "ERROR"}), 400
        
        # Scan
        result = url_scan(sanitized_url)
        
        # Log scan history
        status = result.get("status", "UNKNOWN")
        score = result.get("score", 0)
        confidence = result.get("confidence", "LOW")
        log_scan_history("url", sanitized_url[:100], status, score, confidence)
        
        # Save to database
        save_url_scan(sanitized_url, result)
        
        return jsonify(result)
    
    except Exception as e:
        app_logger.error(f"URL scan error: {str(e)}")
        log_error("URLScanError", str(e), "/check-url", request.remote_addr)
        return jsonify({"error": str(e), "status": "ERROR"}), 500

# ================= EMAIL SCAN (WITH VALIDATION) =================
@app.route("/check-email", methods=["POST"])
def check_email():
    try:
        if not check_api_key():
            return jsonify({"error": "Invalid API Key"}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        email = data.get("email", "")
        
        # Validate email
        is_valid, normalized_email, error_msg = validate_email_address(email)
        if not is_valid:
            return jsonify({"error": error_msg, "status": "ERROR"}), 400
        
        # Scan
        result = email_scan(normalized_email)
        
        # Log scan history
        status = result.get("status", "UNKNOWN")
        score = result.get("score", 0)
        confidence = result.get("confidence", "LOW")
        log_scan_history("email", normalized_email[:100], status, score, confidence)
        
        # Save to database
        save_email_scan(normalized_email, result)
        
        return jsonify(result)
    
    except Exception as e:
        app_logger.error(f"Email scan error: {str(e)}")
        log_error("EmailScanError", str(e), "/check-email", request.remote_addr)
        return jsonify({"error": str(e)}), 500

# ================= CONTENT SCAN (WITH VALIDATION) =================
@app.route("/check-content", methods=["POST"])
def check_content():
    try:
        if not check_api_key():
            return jsonify({"error": "Invalid API Key"}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        text = data.get("text", "")
        
        # Validate content
        is_valid, sanitized_text, error_msg = validate_content(text)
        if not is_valid:
            return jsonify({
                "verdict": "ERROR",
                "score": 0,
                "confidence": "LOW",
                "reasons": [error_msg]
            }), 400
        
        # Scan
        result = content_scan(sanitized_text)
        
        # Log scan history
        verdict = result.get("verdict", "UNKNOWN")
        score = result.get("score", 0)
        confidence = result.get("confidence", "LOW")
        log_scan_history("content", sanitized_text[:100], verdict, score, confidence)
        
        return jsonify(result)
    
    except Exception as e:
        app_logger.error(f"Content scan error: {str(e)}")
        log_error("ContentScanError", str(e), "/check-content", request.remote_addr)
        return jsonify({"error": str(e)}), 500

# ================= PASSWORD CHECK (WITH VALIDATION) =================
@app.route("/check-password", methods=["POST"])
def check_password():
    try:
        if not check_api_key():
            return jsonify({"error": "Invalid API Key"}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        password = data.get("password", "")
        
        # Validate password
        is_valid, sanitized_password, error_msg = validate_password(password)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        from models.password_checker import PasswordChecker
        checker = PasswordChecker()
        result = checker.analyze(sanitized_password)
        
        # Log scan history
        status = result.get("status", "UNKNOWN")
        score = result.get("score", 0)
        confidence = result.get("confidence", "LOW")
        log_scan_history("password", "***", status, score, confidence)
        
        return jsonify(result)
    
    except Exception as e:
        app_logger.error(f"Password check error: {str(e)}")
        log_error("PasswordCheckError", str(e), "/check-password", request.remote_addr)
        return jsonify({"error": str(e)}), 500

# ================= IMAGE SCAN (WITH FILE VALIDATION) =================
@app.route("/check-image", methods=["POST"])
def check_image():
    try:
        if not check_api_key():
            return jsonify({"error": "Invalid API Key"}), 401
        
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        # Validate file
        is_valid, error_msg = validate_image_file(file)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        # Check file size
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({"error": f"File too large. Max {MAX_FILE_SIZE//1024//1024}MB"}), 400
        
        # Scan
        result = scan_image(file)
        
        # Log scan history
        verdict = result.get("verdict", "UNKNOWN")
        score = result.get("score", 0)
        confidence = result.get("confidence", "LOW")
        log_scan_history("image", file.filename[:100], verdict, score, confidence)
        
        return jsonify(result)
    
    except Exception as e:
        app_logger.error(f"Image scan error: {str(e)}")
        log_error("ImageScanError", str(e), "/check-image", request.remote_addr)
        return jsonify({"error": str(e)}), 500

# ================= REPORT SUBMIT =================
@app.route("/submit-report", methods=["POST"])
def submit_report():
    try:
        if not check_api_key():
            return jsonify({"error": "Invalid API Key"}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Sanitize report data
        report_type = sanitize_input(data.get("type", ""))
        report_value = sanitize_input(data.get("value", ""))
        feedback = sanitize_input(data.get("feedback", ""))
        
        log_info(f"Report received - Type: {report_type}")
        
        # Save to database (implement if needed)
        # from services.report_service import save_report
        # save_report(data)
        
        return jsonify({
            "status": "success",
            "message": "Report submitted successfully"
        })
    
    except Exception as e:
        app_logger.error(f"Report submit error: {str(e)}")
        log_error("ReportSubmitError", str(e), "/submit-report", request.remote_addr)
        return jsonify({"error": str(e)}), 500

# ================= AI CHAT =================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        if not check_api_key():
            return jsonify({"reply": "Invalid API Key"}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({"reply": "No data provided"}), 400
        
        user_id = sanitize_input(data.get("user_id", "default"))
        message = sanitize_input(data.get("message", ""))
        
        if not message:
            return jsonify({"reply": "Empty message"}), 400
        
        # Validate message length
        if len(message) > 2000:
            return jsonify({"reply": "Message too long (max 2000 characters)"}), 400
        
        result = process_message(user_id, message)
        
        # Log chat
        log_info(f"Chat - User: {user_id[:20]}, Message: {message[:50]}")
        
        return jsonify(result)
    
    except Exception as e:
        app_logger.error(f"AI Chat error: {str(e)}")
        log_error("AIChatError", str(e), "/chat", request.remote_addr)
        return jsonify({"reply": f"Server error: {str(e)}"}), 500

# ================= HEALTH CHECK =================
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time()
    })

# ================= RUN =================
if __name__ == "__main__":
    print("🚀 PhishGuard Ultra Backend Running on http://localhost:5000")
    print("📋 Endpoints: /check-url, /check-email, /check-content, /check-password, /check-image, /chat")
    app_logger.info("🔥 Server started on port 5000")
    app.run(debug=True, host="0.0.0.0", port=5000)