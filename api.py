import socket
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [response for response in responses if response[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import email_memory
import ai_assistant
from nl_search import execute_nl_query
import subprocess
import sys
from database import get_db_connection
import psycopg2.extras

from pydantic import BaseModel

class LabelRequest(BaseModel):
    name: str

class RuleRequest(BaseModel):
    label: str
    keyword: str

import threading
import time
import subprocess
import sys
from contextlib import asynccontextmanager

def background_automation_loop():
    while True:
        try:
            print("Running background automation loop...")
            subprocess.run([sys.executable, "main.py"])
        except Exception as e:
            print(f"Background loop error: {e}")
        time.sleep(15)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the automation loop in a background thread
    thread = threading.Thread(target=background_automation_loop, daemon=True)
    thread.start()
    yield
    # Shutdown logic if needed

app = FastAPI(lifespan=lifespan)

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/emails")
def get_emails(limit: int = 50):
    return email_memory.get_all_emails_metadata(limit)

@app.get("/api/emails/{email_id}")
def get_email_details(email_id: str):
    data = email_memory.get_email_details(email_id)
    if not data:
        raise HTTPException(status_code=404, detail="Email not found")
    
    data["email_id"] = email_id
    data["tags"] = email_memory.get_email_tags(email_id)
    data["labels"] = email_memory.get_email_labels(email_id)
    email_memory.record_action(email_id, "opened")
    for tag in data["tags"]:
        email_memory.update_interest(tag)
        
    return data

@app.get("/api/deadlines")
def get_deadlines():
    return email_memory.get_all_deadlines()

@app.get("/api/recommended")
def get_recommended():
    return email_memory.get_recommended_emails_metadata()

@app.get("/api/categories")
def get_categories():
    return email_memory.get_category_counts()

@app.get("/api/analytics")
def get_analytics():
    top_interests = [row[0] for row in email_memory.get_top_interests(5)]
    top_tags = email_memory.get_top_tags(10)
    emails_processed = email_memory.get_email_count()
    labels_count = len(email_memory.get_all_labels())
    deadlines_count = len(email_memory.get_all_deadlines())
    
    return {
        "top_interests": top_interests,
        "top_tags": top_tags,
        "emails_processed": emails_processed,
        "labels_count": labels_count,
        "deadlines_count": deadlines_count
    }

@app.get("/api/categories/{category_name}")
def get_emails_by_category(category_name: str):
    email_ids = email_memory.get_emails_by_category(category_name)
    return email_memory.get_emails_metadata_by_ids(email_ids)

@app.get("/api/labels")
def get_labels():
    return email_memory.get_labels()

@app.get("/api/labels/{label_name}")
def get_emails_by_label(label_name: str):
    email_ids = email_memory.get_emails_for_label(label_name)
    return email_memory.get_emails_metadata_by_ids(email_ids)

@app.get("/api/starred")
def get_starred():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email_id FROM emails WHERE is_bookmarked = 1 ORDER BY received_time DESC")
    email_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return email_memory.get_emails_metadata_by_ids(email_ids)

@app.post("/api/toggle-bookmark/{email_id}")
def toggle_bookmark(email_id: str):
    email_memory.toggle_bookmark(email_id)
    return {"status": "success"}

@app.post("/api/search")
def ai_search(query: dict):
    q = query.get("query")
    if not q:
        return []
    results = execute_nl_query(q)
    email_ids = [row[0] for row in results]
    return email_memory.get_emails_metadata_by_ids(email_ids)

@app.post("/api/ask")
def ai_assistant_ask(query: dict):
    q = query.get("query")
    if not q:
        return {"response": "Please provide a query"}
    response = ai_assistant.ask_assistant(q)
    return {"response": response}

@app.post("/api/labels/create")
def api_create_label(req: LabelRequest):
    try:
        email_memory.create_label(req.name)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/rules/create")
def api_create_rule(req: RuleRequest):
    try:
        email_memory.add_rule(req.label, req.keyword)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/refresh")
def refresh_emails():
    try:
        with open("automation_log.txt", "w") as f:
            process = subprocess.run([sys.executable, "main.py"], stdout=f, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
        if process.returncode != 0:
            return {"status": "error", "message": "Sync failed. Check /api/logs"}
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/logs")
def get_logs():
    try:
        with open("automation_log.txt", "r") as f:
            return {"logs": f.read()}
    except Exception:
        return {"logs": "No logs available."}

@app.post("/api/run-automations")
def run_automations_api():
    try:
        from automation_engine import run_all_automations
        run_all_automations()
        return {"status": "success", "message": "Automations executed successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
