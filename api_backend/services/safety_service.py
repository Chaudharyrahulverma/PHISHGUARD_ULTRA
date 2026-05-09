# ========================================
# PHISHGUARD ULTRA - SAFETY SERVICE
# Input Validation, Sanitization, Security Checks
# ========================================

import re
import bleach
from email_validator import validate_email, EmailNotValidError

# ========================================
# ALLOWED TAGS FOR BLEACH (XSS Protection)
# ========================================
ALLOWED_TAGS = []
ALLOWED_ATTRIBUTES = {}

# ========================================
# URL VALIDATION
# ========================================
def validate_url(url):
    """
    Validate and sanitize URL
    Returns: (is_valid, sanitized_url, error_message)
    """
    if not url:
        return False, None, "URL is empty"
    
    if not isinstance(url, str):
        return False, None, "URL must be a string"
    
    url = url.strip()
    
    # Check length
    if len(url) > 2048:
        return False, None, "URL too long (max 2048 characters)"
    
    # Add http:// if no protocol
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    
    # Basic URL pattern check
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        return False, None, "Invalid URL format"
    
    # Sanitize URL
    sanitized = bleach.clean(url, tags=[], strip=True)
    
    return True, sanitized, None

# ========================================
# EMAIL VALIDATION
# ========================================
def validate_email_address(email):
    """
    Validate email address using email-validator library
    Returns: (is_valid, normalized_email, error_message)
    """
    if not email:
        return False, None, "Email is empty"
    
    if not isinstance(email, str):
        return False, None, "Email must be a string"
    
    email = email.strip().lower()
    
    # Check length
    if len(email) > 254:
        return False, None, "Email too long (max 254 characters)"
    
    try:
        # Use email-validator library
        validation = validate_email(email, check_deliverability=False)
        normalized = validation.normalized
        return True, normalized, None
    except EmailNotValidError as e:
        return False, None, str(e)

# ========================================
# TEXT CONTENT VALIDATION
# ========================================
def validate_content(text):
    """
    Validate and sanitize text content
    Returns: (is_valid, sanitized_text, error_message)
    """
    if not text:
        return False, None, "Content is empty"
    
    if not isinstance(text, str):
        return False, None, "Content must be a string"
    
    text = text.strip()
    
    # Check length (max 10000 characters)
    if len(text) > 10000:
        return False, None, "Content too long (max 10000 characters)"
    
    # Sanitize: Remove dangerous HTML/script tags
    sanitized = bleach.clean(text, tags=[], strip=True)
    
    # Remove excessive whitespace
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    return True, sanitized, None

# ========================================
# PASSWORD VALIDATION
# ========================================
def validate_password(password):
    """
    Validate password input
    Returns: (is_valid, sanitized_password, error_message)
    """
    if not password:
        return False, None, "Password is empty"
    
    if not isinstance(password, str):
        return False, None, "Password must be a string"
    
    password = password.strip()
    
    # Check length (max 128 characters)
    if len(password) > 128:
        return False, None, "Password too long (max 128 characters)"
    
    # Remove any non-printable characters
    sanitized = re.sub(r'[^\x20-\x7E]', '', password)
    
    return True, sanitized, None

# ========================================
# IMAGE FILE VALIDATION
# ========================================
def validate_image_file(file):
    """
    Validate uploaded image file
    Returns: (is_valid, error_message)
    """
    if not file:
        return False, "No file provided"
    
    # Check filename
    filename = file.filename if hasattr(file, 'filename') else str(file)
    if not filename:
        return False, "Invalid file"
    
    # Check file extension
    allowed_extensions = ['.png', '.jpg', '.jpeg', '.webp']
    file_ext = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''
    
    if f".{file_ext}" not in allowed_extensions:
        return False, f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
    
    return True, None

# ========================================
# XSS PROTECTION
# ========================================
def sanitize_input(text):
    """
    General input sanitization
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remove HTML tags
    cleaned = bleach.clean(text, tags=[], strip=True)
    
    # Remove potential script patterns
    cleaned = re.sub(r'<script.*?</script>', '', cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r'javascript:', '', cleaned, flags=re.IGNORECASE)
    
    return cleaned.strip()

# ========================================
# RATE LIMIT KEY GENERATOR
# ========================================
def get_rate_limit_key():
    """
    Get rate limit key from request (to be used in app.py)
    """
    from flask import request
    return f"rate_limit:{request.remote_addr}"

# ========================================
# SQL INJECTION PROTECTION (Basic)
# ========================================
def is_sql_injection_attempt(text):
    """
    Detect basic SQL injection patterns
    Returns: True if suspicious, False if safe
    """
    if not text or not isinstance(text, str):
        return False
    
    text = text.lower()
    
    sql_patterns = [
        r"select.*from",
        r"insert.*into",
        r"delete.*from",
        r"drop.*table",
        r"union.*select",
        r"or\s+1\s*=\s*1",
        r"'\s*or\s*'",
        r"--",
        r";"
    ]
    
    for pattern in sql_patterns:
        if re.search(pattern, text):
            return True
    
    return False