import sqlite3

def generate_digest():

    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT category,
           subject,
           deadline
    FROM emails
    ORDER BY relevance DESC
    LIMIT 20
    """)

    rows = cursor.fetchall()

    conn.close()

    digest = "📬 DAILY DIGEST\n\n"

    for row in rows:

        digest += (
            f"[{row[0]}] "
            f"{row[1]}"
        )

        if row[2] not in ("", "NONE"):
            digest += f" | Deadline: {row[2]}"

        digest += "\n"

    return digest