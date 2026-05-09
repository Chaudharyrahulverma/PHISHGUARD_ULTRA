# ========================================
# PHISHGUARD ULTRA - LOGGING SERVICE
# Request Logging, Error Logging, Scan History
# ========================================

import os
import logging
import sqlite3
from datetime import datetime
from logging.handlers import RotatingFileHandler

# ========================================
# DATABASE SETUP FOR LOGS
# ========================================
LOG_DB_PATH = "database/logs.db"

def init_log_database():
    """Initialize logging database tables"""
    os.makedirs("database", exist_ok=True)
    
    conn = sqlite3.connect(LOG_DB_PATH)
    cursor = conn.cursor()
    
    # API Request Logs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT,
            method TEXT,
            ip_address TEXT,
            status_code INTEGER,
            response_time REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Error Logs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS error_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_type TEXT,
            error_message TEXT,
            endpoint TEXT,
            ip_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Scan History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_type TEXT,
            input_value TEXT,
            verdict TEXT,
            score INTEGER,
            confidence TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Logging database initialized")

# ========================================
# FILE LOGGING SETUP (Rotating Logs)
# ========================================
def setup_file_logging():
    """Setup rotating file logging"""
    os.makedirs("logs", exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('PhishGuard')
    logger.setLevel(logging.INFO)
    
    # File handler with rotation (10 MB per file, keep 5 backups)
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create logger instance
app_logger = setup_file_logging()

# ========================================
# LOG TO DATABASE FUNCTIONS
# ========================================
def log_api_request(endpoint, method, ip_address, status_code, response_time):
    """Log API request to database"""
    try:
        conn = sqlite3.connect(LOG_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO api_logs (endpoint, method, ip_address, status_code, response_time)
            VALUES (?, ?, ?, ?, ?)
        """, (endpoint, method, ip_address, status_code, response_time))
        conn.commit()
        conn.close()
    except Exception as e:
        app_logger.error(f"Failed to log API request: {e}")

def log_error(error_type, error_message, endpoint, ip_address):
    """Log error to database"""
    try:
        conn = sqlite3.connect(LOG_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO error_logs (error_type, error_message, endpoint, ip_address)
            VALUES (?, ?, ?, ?)
        """, (error_type, error_message, endpoint, ip_address))
        conn.commit()
        conn.close()
    except Exception as e:
        app_logger.error(f"Failed to log error: {e}")

def log_scan_history(scan_type, input_value, verdict, score, confidence):
    """Log scan history to database"""
    try:
        conn = sqlite3.connect(LOG_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO scan_history (scan_type, input_value, verdict, score, confidence)
            VALUES (?, ?, ?, ?, ?)
        """, (scan_type, input_value, verdict, score, confidence))
        conn.commit()
        conn.close()
    except Exception as e:
        app_logger.error(f"Failed to log scan history: {e}")

# ========================================
# HELPER FUNCTIONS FOR APP.PY
# ========================================
def log_info(message):
    """Log info message"""
    app_logger.info(message)

def log_warning(message):
    """Log warning message"""
    app_logger.warning(message)

def log_error_message(message):
    """Log error message"""
    app_logger.error(message)

def log_debug(message):
    """Log debug message"""
    app_logger.debug(message)

# ========================================
# GET LOGS (For Admin/Reporting)
# ========================================
def get_recent_api_logs(limit=100):
    """Get recent API logs from database"""
    try:
        conn = sqlite3.connect(LOG_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, endpoint, method, ip_address, status_code, response_time, created_at
            FROM api_logs
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        logs = []
        for row in rows:
            logs.append({
                "id": row[0],
                "endpoint": row[1],
                "method": row[2],
                "ip_address": row[3],
                "status_code": row[4],
                "response_time": row[5],
                "created_at": row[6]
            })
        return logs
    except Exception as e:
        app_logger.error(f"Failed to get API logs: {e}")
        return []

def get_recent_error_logs(limit=100):
    """Get recent error logs from database"""
    try:
        conn = sqlite3.connect(LOG_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, error_type, error_message, endpoint, ip_address, created_at
            FROM error_logs
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        logs = []
        for row in rows:
            logs.append({
                "id": row[0],
                "error_type": row[1],
                "error_message": row[2],
                "endpoint": row[3],
                "ip_address": row[4],
                "created_at": row[5]
            })
        return logs
    except Exception as e:
        app_logger.error(f"Failed to get error logs: {e}")
        return []

def get_recent_scan_history(limit=100):
    """Get recent scan history from database"""
    try:
        conn = sqlite3.connect(LOG_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, scan_type, input_value, verdict, score, confidence, created_at
            FROM scan_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        scans = []
        for row in rows:
            scans.append({
                "id": row[0],
                "scan_type": row[1],
                "input_value": row[2],
                "verdict": row[3],
                "score": row[4],
                "confidence": row[5],
                "created_at": row[6]
            })
        return scans
    except Exception as e:
        app_logger.error(f"Failed to get scan history: {e}")
        return []

# ========================================
# CLEAN OLD LOGS (Optional)
# ========================================
def clean_old_logs(days=30):
    """Delete logs older than specified days"""
    try:
        conn = sqlite3.connect(LOG_DB_PATH)
        cursor = conn.cursor()
        
        from datetime import datetime, timedelta
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute("DELETE FROM api_logs WHERE created_at < ?", (cutoff_date,))
        cursor.execute("DELETE FROM error_logs WHERE created_at < ?", (cutoff_date,))
        cursor.execute("DELETE FROM scan_history WHERE created_at < ?", (cutoff_date,))
        
        conn.commit()
        conn.close()
        
        app_logger.info(f"Cleaned logs older than {days} days")
    except Exception as e:
        app_logger.error(f"Failed to clean old logs: {e}")

# ========================================
# INITIALIZE ON IMPORT
# ========================================
init_log_database()
app_logger.info("🚀 Logging Service Initialized")