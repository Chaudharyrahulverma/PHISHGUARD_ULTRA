import sqlite3

conn = sqlite3.connect("database/db.sqlite3")
cur = conn.cursor()

cur.execute("SELECT * FROM url_scans ORDER BY id DESC LIMIT 20")
rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()