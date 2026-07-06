import sys
import time
from datetime import datetime
from gmail_reader import get_latest_emails
from gmail_service import get_gmail_service
from ai_agent import analyze_email
from calendar_service import get_calendar_service
from calendar_manager import create_event
from calendar_memory import event_exists, save_event
from label_manager import get_or_create_label, apply_label
from email_memory import (
    email_exists, save_email, save_tag, assign_label,
    get_all_labels, get_rules, get_interest_score, calculate_importance as calc_imp
)
from database import get_db_connection

sys.stdout.reconfigure(encoding="utf-8")

def auto_assign_labels(user_id, email_id, subject, body):
    text = (subject + " " + body).lower()
    labels = get_all_labels(user_id)
    for label in labels:
        rules = get_rules(user_id, label)
        for keyword in rules:
            if keyword.lower() in text:
                assign_label(user_id, email_id, label)
                print(f"Assigned '{label}' -> {subject}")
                break

def get_deadline_score(deadline):
    if deadline == "NONE" or deadline == "": return 0
    try:
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
        today = datetime.today().date()
        days = (deadline_date - today).days
        if days <= 0: return 20
        elif days <= 1: return 15
        elif days <= 3: return 10
        elif days <= 7: return 5
        return 0
    except: return 0

def calculate_importance(user_id, result, email):
    relevance = result.get("relevance", 0)
    interest_score = 0
    for tag in result.get("tags", []):
        interest_score += get_interest_score(user_id, tag)
    deadline_score = get_deadline_score(result.get("deadline", "NONE"))
    
    return calc_imp(
        relevance=relevance,
        deadline_score=deadline_score,
        interest_score=interest_score,
        action_score=0,
        received_time=email.get("timestamp"),
        is_bookmarked=0
    )

def process_user(user_id, refresh_token):
    service = get_gmail_service(refresh_token)
    calendar_service = get_calendar_service(refresh_token)
    emails = get_latest_emails(service, 50)
    
    print(f"Checking {len(emails)} recent emails for user {user_id}...")
    processed_count = 0
    
    for email in emails:
        ai_limit_reached = False

        if email_exists(user_id, email["id"]):
            print(f"Skipping: {email['subject']}")
            continue

        print(f"PROCESSING NEW EMAIL: {email['subject']}")
        try:
            if processed_count > 0: time.sleep(3)
            
            ai_category = "Uncategorized"
            ai_summary = "AI Analysis Pending / Skipped"
            ai_deadline = "NONE"
            ai_relevance = 0
            ai_importance = 0
            ai_action = "NONE"

            if processed_count >= 5:
                print("Batch limit reached (5). Waiting for next cycle to respect rate limits.")
                break
                
            if not ai_limit_reached:
                try:
                    result = analyze_email(email["subject"], email["body"][:3000])
                    processed_count += 1
                    
                    for tag in result.get("tags", []):
                        save_tag(user_id, email["id"], tag)

                    print("\nAI RESULT:")
                    print(result)

                    if result["deadline"] not in ["NONE", ""]:
                        if not event_exists(user_id, email["id"]):
                            try:
                                create_event(calendar_service, email["subject"], result["deadline"])
                                save_event(user_id, email["id"], email["subject"])
                            except Exception as e:
                                print(f"Calendar Error: {e}")

                    if result["category"] == "IGNORE":
                        continue

                    label_id = get_or_create_label(service, result["category"])
                    apply_label(service, email["id"], label_id)
                    
                    ai_category = result["category"]
                    ai_summary = result["summary"]
                    ai_deadline = result["deadline"]
                    ai_relevance = result["relevance"]
                    ai_importance = calculate_importance(user_id, result, email)
                    ai_action = result.get("adaptive_action", "NONE")
                except Exception as e:
                    if "RATE_LIMIT" in str(e):
                        raise
                    print(f"AI Processing Skipped/Failed for {email['subject']}: {e}")

            save_email(
                user_id, email["id"], email["subject"], email["body"],
                ai_category, ai_summary, ai_deadline, ai_relevance,
                ai_importance, email["timestamp"], ai_action
            )
            auto_assign_labels(user_id, email["id"], email["subject"], email["body"])
            
        except Exception as e:
            if "RATE_LIMIT" in str(e):
                print("Groq rate limit hit. Pausing processing for this cycle.")
                break
            print(f"\nERROR PROCESSING EMAIL: {e}")
            continue

    try:
        from automation_engine import run_all_automations
        run_all_automations() # Note: automation_engine also needs user_id in the future
    except Exception as e:
        print(f"Failed to run automations: {e}")

def main():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, refresh_token FROM users")
    users = cursor.fetchall()
    conn.close()
    
    for user_id, refresh_token in users:
        print(f"=============================")
        print(f"Processing user {user_id}...")
        process_user(user_id, refresh_token)
        print(f"=============================")

if __name__ == "__main__":
    main()
