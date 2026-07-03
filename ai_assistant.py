import requests
import json
from database import get_db_connection
import psycopg2.extras
from datetime import datetime
from nl_search import execute_nl_query
from email_memory import get_emails_metadata_by_ids

OLLAMA_URL = "http://localhost:11434/api/generate"

def get_context(user_query):
    """Fetch relevant context dynamically based on the user's query."""
    # RAG Step 1: Use the query to fetch specific contextual emails
    results = execute_nl_query(user_query)
    
    if not results:
        # Fallback to default high-priority context if no specific results
        conn = get_db_connection()
        cursor = conn.cursor()
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        cursor.execute("""
        SELECT subject, deadline, summary 
        FROM emails 
        WHERE deadline IS NOT NULL 
          AND deadline != 'NONE' 
          AND deadline != ''
          AND deadline >= %s
        ORDER BY deadline ASC LIMIT 10
        """, (today_str,))
        deadlines = cursor.fetchall()
        
        cursor.execute("""
        SELECT subject, category, summary, importance 
        FROM emails 
        ORDER BY importance DESC LIMIT 10
        """)
        important = cursor.fetchall()
        conn.close()
        
        context = "UPCOMING DEADLINES:\n"
        for d in deadlines:
            context += f"- {d[0]} (Deadline: {d[1]}): {d[2]}\n"
            
        context += "\nHIGH IMPORTANCE EMAILS:\n"
        for i in important:
            context += f"- [{i[1]}] {i[0]} (Score: {i[3]}): {i[2]}\n"
            
        return context

    # RAG Step 2: Format the dynamically retrieved emails
    email_ids = [row[0] for row in results[:15]] # Cap at 15 to fit in prompt
    emails = get_emails_metadata_by_ids(email_ids)
    
    context = "RELEVANT EMAILS FOR THE USER'S QUERY:\n"
    for e in emails:
        context += f"- Subject: {e['subject']}\n"
        context += f"  Summary: {e['summary']}\n"
        if e['deadline'] and e['deadline'] != 'NONE':
            context += f"  Deadline: {e['deadline']}\n"
        context += f"  Category: {e['category']} | Priority: {e['priority']}\n\n"
        
    return context

def ask_assistant(user_query):
    context = get_context(user_query)
    today = datetime.now().strftime("%Y-%m-%d")
    
    prompt = f"""
You are an intelligent AI Assistant for a communication platform.
Today is {today}.

Based on the following retrieved email context, answer the user's question accurately and concisely.

TEMPORAL RULES:
- Strictly ignore any deadlines before {today}.
- "Tomorrow" is { (datetime.now().fromtimestamp(datetime.now().timestamp() + 86400)).strftime("%Y-%m-%d") }.
- If the user asks about deadlines, list them clearly starting from the closest one.
- You must ONLY use the provided context. Do not invent information.

CONTEXT:
{context}

USER QUESTION: {user_query}

ASSISTANT RESPONSE:
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
        return data["response"].strip()
    except Exception as e:
        return f"Error: {e}"
