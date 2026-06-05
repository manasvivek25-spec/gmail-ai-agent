import sqlite3

conn = sqlite3.connect("emails.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS emails (
    email_id TEXT PRIMARY KEY,
    subject TEXT,
    body TEXT,
    category TEXT,
    summary TEXT,
    deadline TEXT,
    relevance REAL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS calendar_events (
    email_id TEXT PRIMARY KEY,
    event_name TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully.")