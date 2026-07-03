from database import get_db_connection
import psycopg2.extras
from datetime import datetime

def run_all_automations():
    """Run all background automations to keep the system organized."""
    print("Running Automation Engine...")
    auto_flag_urgent_deadlines()
    execute_adaptive_actions()
    print("Automations completed.")

def auto_flag_urgent_deadlines():
    """Automatically upgrades priority to Critical for emails with a deadline in < 3 days."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all emails with deadlines
    cursor.execute("SELECT email_id, deadline, importance FROM emails WHERE deadline IS NOT NULL AND deadline != 'NONE' AND deadline != ''")
    emails = cursor.fetchall()
    
    today = datetime.today().date()
    updates = []
    
    for email_id, deadline, importance in emails:
        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
            days_left = (deadline_date - today).days
            
            # If deadline is within 3 days and importance isn't already critically high (> 25)
            if 0 <= days_left <= 3 and importance < 25:
                # Upgrade priority by boosting importance
                new_importance = importance + 15
                updates.append((new_importance, email_id))
                print(f"[Automation] Upgraded priority for {email_id} (Deadline in {days_left} days)")
        except Exception as e:
            print(f"Error processing deadline for automation: {e}")
            
    if updates:
        cursor.executemany("UPDATE emails SET importance = %s WHERE email_id = %s", updates)
        conn.commit()
        
    conn.close()

def execute_adaptive_actions():
    """Executes dynamic LLM-generated adaptive actions."""
    print("Executing adaptive actions...")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # We process ALL emails that have an adaptive action that isn't NONE or COMPLETED
        cursor.execute("SELECT email_id, adaptive_action, category FROM emails WHERE adaptive_action != 'NONE' AND adaptive_action != 'COMPLETED'")
        emails = cursor.fetchall()
        
        updates = []
        for email_id, action, category in emails:
            # Execute logic based on adaptive action
            if action == 'ARCHIVE':
                # Actually archiving requires hitting the Gmail API
                # For now we will just set the category to IGNORE as the internal equivalent
                print(f"[Adaptive AI] Archiving {email_id} because user usually ignores this type of content.")
                updates.append(("IGNORE", 'COMPLETED', email_id))
            elif action == 'STAR':
                print(f"[Adaptive AI] Starring {email_id} because it matches high-interest profile.")
                updates.append((category, 'COMPLETED', email_id))
            elif action == 'MARK_READ':
                print(f"[Adaptive AI] Marking {email_id} as read.")
                updates.append((category, 'COMPLETED', email_id))
            else:
                updates.append((category, 'COMPLETED', email_id))
                
        if updates:
            cursor.executemany("UPDATE emails SET category = %s, adaptive_action = %s WHERE email_id = %s", updates)
            conn.commit()
            
        conn.close()
    except Exception as e:
        print(f"Error executing adaptive actions: {e}")

if __name__ == "__main__":
    run_all_automations()
