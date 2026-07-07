import socket
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [response for response in responses if response[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

from fastapi import FastAPI, HTTPException, Depends
from auth import router as auth_router, get_current_user
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
app.include_router(auth_router)

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/emails")
def get_emails(limit: int = 50, user_id: str = Depends(get_current_user)):
    return email_memory.get_all_emails_metadata(user_id, limit)

@app.get("/api/emails/{email_id}")
def get_email_details(email_id: str, user_id: str = Depends(get_current_user)):
    data = email_memory.get_email_details(user_id, email_id)
    if not data:
        raise HTTPException(status_code=404, detail="Email not found")
    
    data["email_id"] = email_id
    data["tags"] = email_memory.get_email_tags(user_id, email_id)
    data["labels"] = email_memory.get_email_labels(user_id, email_id)
    email_memory.record_action(user_id, email_id, "opened")
    for tag in data["tags"]:
        email_memory.update_interest(user_id, tag)
        
    return data

@app.get("/api/deadlines")
def get_deadlines(user_id: str = Depends(get_current_user)):
    return email_memory.get_all_deadlines(user_id, )

@app.get("/api/recommended")
def get_recommended(user_id: str = Depends(get_current_user)):
    return email_memory.get_recommended_emails_metadata(user_id, )

@app.get("/api/categories")
def get_categories(user_id: str = Depends(get_current_user)):
    return email_memory.get_category_counts(user_id, )

@app.get("/api/analytics")
def get_analytics(user_id: str = Depends(get_current_user)):
    top_interests = [row[0] for row in email_memory.get_top_interests(user_id, 5)]
    top_tags = email_memory.get_top_tags(user_id, 10)
    emails_processed = email_memory.get_email_count(user_id, )
    labels_count = len(email_memory.get_all_labels(user_id, ))
    deadlines_count = len(email_memory.get_all_deadlines(user_id, ))
    
    return {
        "top_interests": top_interests,
        "top_tags": top_tags,
        "emails_processed": emails_processed,
        "labels_count": labels_count,
        "deadlines_count": deadlines_count
    }

@app.get("/api/categories/{category_name}")
def get_emails_by_category(category_name: str, user_id: str = Depends(get_current_user)):
    email_ids = email_memory.get_emails_by_category(user_id, category_name)
    return email_memory.get_emails_metadata_by_ids(user_id, email_ids)

@app.get("/api/labels")
def get_labels(user_id: str = Depends(get_current_user)):
    return email_memory.get_labels(user_id, )

@app.get("/api/labels/{label_name}")
def get_emails_by_label(label_name: str, user_id: str = Depends(get_current_user)):
    email_ids = email_memory.get_emails_for_label(user_id, label_name)
    return email_memory.get_emails_metadata_by_ids(user_id, email_ids)

@app.get("/api/starred")
def get_starred(user_id: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email_id FROM emails WHERE user_id=%s AND is_bookmarked = 1 ORDER BY received_time DESC", (user_id,))
    email_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    return email_memory.get_emails_metadata_by_ids(user_id, email_ids)

@app.post("/api/toggle-bookmark/{email_id}")
def toggle_bookmark(email_id: str, user_id: str = Depends(get_current_user)):
    email_memory.toggle_bookmark(user_id, email_id)
    return {"status": "success"}

@app.post("/api/search")
def ai_search(query: dict, user_id: str = Depends(get_current_user)):
    q = query.get("query")
    if not q:
        return []
    results = execute_nl_query(q)
    email_ids = [row[0] for row in results]
    return email_memory.get_emails_metadata_by_ids(user_id, email_ids)

@app.post("/api/ask")
def ai_assistant_ask(query: dict, user_id: str = Depends(get_current_user)):
    q = query.get("query")
    if not q:
        return {"response": "Please provide a query"}
    response = ai_assistant.ask_assistant(q)
    return {"response": response}

@app.post("/api/labels/create")
def api_create_label(req: LabelRequest, user_id: str = Depends(get_current_user)):
    try:
        email_memory.create_label(user_id, req.name)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/rules/create")
def api_create_rule(req: RuleRequest, user_id: str = Depends(get_current_user)):
    try:
        email_memory.add_rule(user_id, req.label, req.keyword)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

from fastapi import BackgroundTasks

@app.post("/api/refresh")
def refresh_emails(user_id: str = Depends(get_current_user)):
    try:
        from main import process_user
        from database import get_db_connection
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT refresh_token FROM users WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return {"status": "error", "message": "User not found"}
            
        refresh_token = row[0]
        
        # Run synchronously so the client waits for the sync to complete before refetching
        process_user(user_id, refresh_token)
        
        return {"status": "success", "message": "Sync completed successfully. Inbox updated."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/logs")
def get_logs(user_id: str = Depends(get_current_user)):
    try:
        with open("automation_log.txt", "r") as f:
            return {"logs": f.read()}
    except Exception:
        return {"logs": "No logs available."}

@app.post("/api/run-automations")
def run_automations_api(user_id: str = Depends(get_current_user)):
    try:
        from automation_engine import run_all_automations
        run_all_automations()
        return {"status": "success", "message": "Automations executed successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

dist_dir = os.path.join(os.path.dirname(__file__), "frontend", "dist")
if os.path.exists(dist_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(dist_dir, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/") or full_path.startswith("auth/"):
            return {"detail": "Not Found"}
        
        file_path = os.path.join(dist_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(dist_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
