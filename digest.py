from database import get_db_connection
import psycopg2.extras


def generate_digest():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT subject,
           category,
           summary,
           deadline,
           relevance
    FROM emails
    ORDER BY relevance DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    seen_subjects = set()

    deadline_emails = []

    categories = {
        "INTERNSHIP": [],
        "ACADEMIC": [],
        "EVENT": [],
        "MESS": [],
        "IGNORE": []
    }

    for row in rows:

        subject = row[0]
        category = row[1]
        summary = row[2]
        deadline = row[3]
        relevance = row[4]

        # Clean deadline field
        if deadline is None:
            deadline = "NONE"

        deadline = str(deadline).strip()

        if deadline.upper().startswith("NONE"):
            deadline = "NONE"

        # Remove duplicates
        if subject in seen_subjects:
            continue

        seen_subjects.add(subject)

        email_data = {
            "subject": subject,
            "summary": summary,
            "deadline": deadline,
            "relevance": relevance
        }

        if deadline != "NONE":
            deadline_emails.append(email_data)

        if category in categories:
            categories[category].append(email_data)
        else:
            categories["EVENT"].append(email_data)

    print("\n" + "=" * 70)
    print("📬 TODAY'S DIGEST")
    print("=" * 70)

    # INTERNSHIPS
    print("\n🔥 INTERNSHIPS & CAREER\n")

    for email in categories["INTERNSHIP"]:

        print(f"• {email['subject']}")

        if email["deadline"] != "NONE":
            print(f"  Deadline: {email['deadline']}")

        print(f"  Summary: {email['summary']}")
        print()

    # ACADEMICS
    print("\n📚 ACADEMICS\n")

    for email in categories["ACADEMIC"]:

        print(f"• {email['subject']}")

        if email["deadline"] != "NONE":
            print(f"  Deadline: {email['deadline']}")

        print(f"  Summary: {email['summary']}")
        print()

    # EVENTS
    print("\n🎯 EVENTS\n")

    for email in categories["EVENT"]:

        print(f"• {email['subject']}")

        if email["deadline"] != "NONE":
            print(f"  Deadline: {email['deadline']}")

        print(f"  Summary: {email['summary']}")
        print()

    # MESS
    print("\n🍽 MESS NOTICES\n")

    for email in categories["MESS"]:
        print(f"• {email['subject']}")

    # IGNORE
    print("\n🗑 IGNORED EMAILS\n")

    for email in categories["IGNORE"]:
        print(f"• {email['subject']}")

    print("\n" + "=" * 70)

    # DEADLINE DASHBOARD
    print("\n⏰ UPCOMING DEADLINES\n")

    if len(deadline_emails) == 0:

        print("No deadlines found.")

    else:

        for email in deadline_emails:

            print(f"• {email['subject']}")
            print(f"  Deadline: {email['deadline']}")
            print()

    print("=" * 70)