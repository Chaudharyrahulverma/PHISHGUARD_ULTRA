import sqlite3

DB_PATH = "database/db.sqlite3"


def save_report(data):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reports 
        (type, value, wrong_detection, missing_reason, poor_explanation, feedback)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get("type"),
        data.get("value"),
        int(data.get("wrong_detection", False)),
        int(data.get("missing_reason", False)),
        int(data.get("poor_explanation", False)),
        data.get("feedback")
    ))

    conn.commit()
    conn.close()

    return {"status": "success", "message": "Report saved"}