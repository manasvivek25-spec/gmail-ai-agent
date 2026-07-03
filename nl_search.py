
import requests
import json
from database import get_db_connection
import psycopg2.extras

OLLAMA_URL = "http://localhost:11434/api/generate"

SCHEMA = """
Table: emails
Columns: email_id, subject, body, category, summary, deadline, relevance, importance, received_time, is_bookmarked

Table: email_tags
Columns: email_id, tag

Table: user_labels
Columns: id, label_name

Table: email_labels
Columns: email_id, label_name

Table: user_actions
Columns: email_id, action, action_time

Table: user_interests
Columns: keyword, score
"""

def get_sql_query(user_query):
    prompt = f"""
You are an expert SQL assistant for a communication application.
Given the following SQLite schema:
{SCHEMA}

Translate the user's natural language request into a valid SQLite SELECT query.
The query MUST return at least the 'email_id' and 'subject' columns from the 'emails' table as the first two columns.
The query should ONLY select from the 'emails' table, although it can JOIN with other tables for filtering.
Return ONLY the SQL query, nothing else. No markdown formatting, no explanations.
The query MUST be read-only (SELECT only).

User Request: {user_query}

SQL Query:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        sql = data["response"].strip()
        
        # Basic sanitization: ensure it starts with SELECT and doesn't contain destructive commands
        sql_upper = sql.upper()
        if not sql_upper.startswith("SELECT"):
            raise Exception("Generated query is not a SELECT statement.")
        
        forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE"]
        for cmd in forbidden:
            if cmd in sql_upper:
                raise Exception(f"Generated query contains forbidden command: {cmd}")
                
        return sql
    except Exception as e:
        print(f"NL Search Error: {e}")
        return None

def execute_nl_query(user_query):
    sql = get_sql_query(user_query)
    if not sql:
        return []

    print(f"EXECUTING SQL: {sql}")
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        print(f"SQL Execution Error: {e}")
        return []

if __name__ == "__main__":
    # Test queries
    test_queries = [
        "Show all internships",
        "Emails with deadlines this week",
        "Show my bookmarked emails",
        "Highest importance emails"
    ]
    for q in test_queries:
        print(f"\nQuery: {q}")
        results = execute_nl_query(q)
        print(f"Found {len(results)} results.")
