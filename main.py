import socket
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [response for response in responses if response[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

from gmail_reader import get_latest_emails
from gmail_service import get_gmail_service
from ai_agent import analyze_email

from calendar_service import get_calendar_service
from calendar_manager import create_event

from calendar_memory import (
    event_exists,
    save_event
)


from label_manager import (
    get_or_create_label,
    apply_label
)
from email_memory import (
    email_exists,
    save_email,
    save_tag,
    assign_label,
    get_all_labels,
    get_rules,
    get_interest_score
)
import sys

sys.stdout.reconfigure(encoding="utf-8")
def auto_assign_labels(
    email_id,
    subject,
    body
):

    text = (
        subject + " " + body
    ).lower()

    labels = get_all_labels()

    for label in labels:

        rules = get_rules(label)

        for keyword in rules:

            if keyword.lower() in text:

                assign_label(
                    email_id,
                    label
                )

                print(
                    f"Assigned '{label}' -> {subject}"
                )

                break
# Gmail Service
service = get_gmail_service()

# Calendar Service
calendar_service = get_calendar_service()

# Get latest emails
emails = get_latest_emails(50)
from datetime import datetime


def get_deadline_score(
    deadline
):

    if (
        deadline == "NONE"
        or
        deadline == ""
    ):
        return 0

    try:

        deadline_date = datetime.strptime(
            deadline,
            "%Y-%m-%d"
        ).date()

        today = datetime.today().date()

        days = (
            deadline_date - today
        ).days

        if days <= 0:
            return 20

        elif days <= 1:
            return 15

        elif days <= 3:
            return 10

        elif days <= 7:
            return 5

        return 0

    except:
        return 0
def calculate_importance(
    result,
    email
):

    relevance = result.get("relevance", 0)

    interest_score = 0
    for tag in result.get("tags", []):
        interest_score += get_interest_score(tag)

    deadline_score = get_deadline_score(result.get("deadline", "NONE"))

    # For new emails, action_score and recency_score are 0 initially
    # but we can add a base recency score if we wanted to.
    # We will use the centralized formula logic here.
    
    from email_memory import calculate_importance as calc_imp

    return calc_imp(
        relevance=relevance,
        deadline_score=deadline_score,
        interest_score=interest_score,
        action_score=0,
        received_time=email.get("timestamp"),
        is_bookmarked=0
    )

print(f"Checking {len(emails)} recent emails for new messages...")

processed_count = 0
import time
for email in emails:

    if processed_count >= 5:
        print("Batch limit reached (5). Waiting for next cycle to respect rate limits.")
        break

    if email_exists(email["id"]):

        print(
            f"Skipping: {email['subject']}"
        )

        continue

    print(f"PROCESSING NEW EMAIL: {email['subject']}")

    # Add a small delay between requests to avoid TPM limits
    if processed_count > 0:
        time.sleep(3)

    try:
        # AI Analysis
        result = analyze_email(
            email["subject"],
            email["body"][:3000]
        )
        
        processed_count += 1
        
        for tag in result.get("tags", []):
            save_tag(email["id"], tag)

        print("\nAI RESULT:")
        print(result)

        # Calendar Integration
        if result["deadline"] != "NONE" and result["deadline"] != "":
            if not event_exists(email["id"]):
                try:
                    create_event(calendar_service, email["subject"], result["deadline"])
                    save_event(email["id"], email["subject"])
                except Exception as e:
                    print(f"Calendar Error: {e}")

        # Ignore category
        if result["category"] == "IGNORE":
            print(f"WOULD ARCHIVE: {email['subject']}")
            continue

        # Gmail Labels
        label_id = get_or_create_label(service, result["category"])
        apply_label(service, email["id"], label_id)
        
        importance = calculate_importance(result, email)
        
        # Save Email
        save_email(
            email["id"],
            email["subject"],
            email["body"],
            result["category"],
            result["summary"],
            result["deadline"],
            result["relevance"],
            importance,
            email["timestamp"],
            result.get("adaptive_action", "NONE")
        )
        
        auto_assign_labels(email["id"], email["subject"], email["body"])
        print(f"Label assignment completed for: {email['subject']}")
        print("\n" + "=" * 70)
        print("SUBJECT:")
        print(email["subject"])
        print("\nCATEGORY:")
        print(result["category"])
        print("\nSUMMARY:")
        print(result["summary"])
        print("\nDEADLINE:")
        print(result["deadline"])
        print("\nRELEVANCE:")
        print(result["relevance"])
        print("=" * 70)

    except Exception as e:
        if "RATE_LIMIT" in str(e):
            print("Groq rate limit hit. Pausing processing for this cycle.")
            break
        else:
            print("\nERROR PROCESSING EMAIL:")
            print(email["subject"])
            print("\nERROR:")
            print(e)
            continue

# Run Background Automations after syncing
try:
    from automation_engine import run_all_automations
    run_all_automations()
except Exception as e:
    print(f"Failed to run automations: {e}")
