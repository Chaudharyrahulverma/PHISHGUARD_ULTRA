import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "db.sqlite3")

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS url_scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        status TEXT,
        score INTEGER,
        confidence TEXT,
        reasons TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_url_scan(url, result):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO url_scans (url, status, score, confidence, reasons, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        url,
        result.get("status"),
        result.get("score"),
        result.get("confidence"),
        ", ".join(result.get("reasons", [])),
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()