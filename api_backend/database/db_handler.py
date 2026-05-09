import sqlite3

DB_PATH = "database/db.sqlite3"


# =========================
# CONNECTION
# =========================
def get_connection():
    return sqlite3.connect(DB_PATH)


# =========================
# INIT DATABASE
# =========================
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # -------------------------
    # URL SCANS
    # -------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS url_scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT UNIQUE,
        status TEXT,
        score INTEGER,
        confidence TEXT,
        reasons TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -------------------------
    # EMAIL SCANS
    # -------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS email_scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        status TEXT,
        score INTEGER,
        confidence TEXT,
        reasons TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -------------------------
    # CONTENT SCANS
    # -------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS content_scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT UNIQUE,
        status TEXT,
        score INTEGER,
        confidence TEXT,
        reasons TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -------------------------
    # PASSWORD SCANS (FUTURE READY)
    # -------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS password_scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        password TEXT UNIQUE,
        strength TEXT,
        score INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -------------------------
    # REPORTS (SELF LEARNING)
    # -------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        value TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# =========================
# SAVE FUNCTIONS
# =========================

def save_url_scan(url, result):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        INSERT INTO url_scans (url, status, score, confidence, reasons)
        VALUES (?, ?, ?, ?, ?)
        """, (
            url,
            result.get("status"),
            result.get("score"),
            result.get("confidence"),
            ", ".join(result.get("reasons", []))
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        print("⚠️ Duplicate URL skipped:", url)

    conn.close()


def save_email_scan(email, result):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        INSERT INTO email_scans (email, status, score, confidence, reasons)
        VALUES (?, ?, ?, ?, ?)
        """, (
            email,
            result.get("status"),
            result.get("score"),
            result.get("confidence"),
            ", ".join(result.get("reasons", []))
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        print("⚠️ Duplicate email skipped:", email)

    conn.close()


def save_content_scan(text, result):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        INSERT INTO content_scans (text, status, score, confidence, reasons)
        VALUES (?, ?, ?, ?, ?)
        """, (
            text,
            result.get("status"),
            result.get("score"),
            result.get("confidence"),
            ", ".join(result.get("reasons", []))
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        print("⚠️ Duplicate content skipped")

    conn.close()


def save_password_scan(password, strength, score):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        INSERT INTO password_scans (password, strength, score)
        VALUES (?, ?, ?)
        """, (
            password,
            strength,
            score
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        print("⚠️ Duplicate password skipped")

    conn.close()


# =========================
# REPORT STORAGE
# =========================
def save_report(report_type, value, message):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO reports (type, value, message)
    VALUES (?, ?, ?)
    """, (report_type, value, message))

#add 
def create_report_table():
    import sqlite3
    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        value TEXT,
        wrong_detection INTEGER,
        missing_reason INTEGER,
        poor_explanation INTEGER,
        feedback TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    
    

    conn.commit()
    conn.close()
    