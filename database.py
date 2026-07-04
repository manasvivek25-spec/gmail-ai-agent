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
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        refresh_token TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        user_id TEXT REFERENCES users(user_id) ON DELETE CASCADE,
        email_id TEXT,
        subject TEXT,
        body TEXT,
        category TEXT,
        summary TEXT,
        deadline TEXT,
        relevance REAL,
        importance REAL DEFAULT 0,
        received_time BIGINT,
        is_bookmarked INTEGER DEFAULT 0,
        adaptive_action TEXT,
        PRIMARY KEY (user_id, email_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calendar_events (
        user_id TEXT REFERENCES users(user_id) ON DELETE CASCADE,
        email_id TEXT,
        event_name TEXT,
        PRIMARY KEY (user_id, email_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_labels (
        id SERIAL PRIMARY KEY,
        user_id TEXT REFERENCES users(user_id) ON DELETE CASCADE,
        label_name TEXT NOT NULL,
        UNIQUE (user_id, label_name)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS label_rules (
        id SERIAL PRIMARY KEY,
        user_id TEXT REFERENCES users(user_id) ON DELETE CASCADE,
        label_name TEXT NOT NULL,
        keyword TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_labels (
        user_id TEXT REFERENCES users(user_id) ON DELETE CASCADE,
        email_id TEXT,
        label_name TEXT,
        PRIMARY KEY (user_id, email_id, label_name)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_tags (
        user_id TEXT REFERENCES users(user_id) ON DELETE CASCADE,
        email_id TEXT,
        tag TEXT,
        PRIMARY KEY (user_id, email_id, tag)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_actions (
        user_id TEXT REFERENCES users(user_id) ON DELETE CASCADE,
        email_id TEXT,
        action TEXT,
        action_time TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_interests (
        user_id TEXT REFERENCES users(user_id) ON DELETE CASCADE,
        keyword TEXT,
        score INTEGER DEFAULT 1,
        PRIMARY KEY (user_id, keyword)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("Multi-tenant PostgreSQL Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()

