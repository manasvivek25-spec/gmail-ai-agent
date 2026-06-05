from gmail_reader import get_latest_emails
from gmail_service import get_gmail_service
from ai_agent import analyze_email

from calendar_service import get_calendar_service
from calendar_manager import create_event

from calendar_memory import (
    event_exists,
    save_event
)

from email_memory import (
    email_exists,
    save_email
)

from label_manager import (
    get_or_create_label,
    apply_label
)

# Gmail
service = get_gmail_service()

# Google Calendar
calendar_service = get_calendar_service()

# Latest emails
emails = get_latest_emails(20)

for email in emails:

    if email_exists(email["id"]):
        print(f"Skipping: {email['subject']}")
        continue

    try:

        # AI Analysis
        result = analyze_email(
            email["subject"],
            email["body"][:3000]
        )

        print("\nAI RESULT:")
        print(result)

        # Calendar Integration
        if (
            result["deadline"] != "NONE"
            and
            result["deadline"] != ""
        ):

            if not event_exists(email["id"]):

                try:

                    create_event(
                        calendar_service,
                        email["subject"],
                        result["deadline"]
                    )

                    save_event(
                        email["id"],
                        email["subject"]
                    )

                    print(
                        f"Calendar Event Created: {email['subject']}"
                    )

                except Exception as e:

                    print(
                        f"Calendar Error: {e}"
                    )

        # Ignore emails
        if result["category"] == "IGNORE":

            print(
                f"WOULD ARCHIVE: {email['subject']}"
            )

            continue

        # Gmail Label
        label_id = get_or_create_label(
            service,
            result["category"]
        )

        apply_label(
            service,
            email["id"],
            label_id
        )

        # Save to database
        save_email(
            email["id"],
            email["subject"],
            email["body"],
            result["category"],
            result["summary"],
            result["deadline"],
            result["relevance"]
        )

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

        print("\nERROR PROCESSING EMAIL:")
        print(email["subject"])

        print("\nERROR:")
        print(e)