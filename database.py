import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(os.environ.get("SUPABASE_URL"))

def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        email_id TEXT PRIMARY KEY,
        subject TEXT,
        body TEXT,
        category TEXT,
        summary TEXT,
        deadline TEXT,
        relevance REAL,
        importance REAL DEFAULT 0,
        received_time BIGINT,
        is_bookmarked INTEGER DEFAULT 0,
        adaptive_action TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calendar_events (
        email_id TEXT PRIMARY KEY,
        event_name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_labels (
        id SERIAL PRIMARY KEY,
        label_name TEXT UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS label_rules (
        id SERIAL PRIMARY KEY,
        label_name TEXT NOT NULL,
        keyword TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_labels (
        email_id TEXT,
        label_name TEXT,
        PRIMARY KEY (email_id, label_name)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_tags (
        email_id TEXT,
        tag TEXT,
        PRIMARY KEY (email_id, tag)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_actions (
        email_id TEXT,
        action TEXT,
        action_time TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_interests (
        keyword TEXT PRIMARY KEY,
        score INTEGER DEFAULT 1
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("PostgreSQL (Supabase) Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
