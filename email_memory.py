import sqlite3


def email_exists(email_id):

    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email_id FROM emails WHERE email_id=?",
        (email_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


def save_email(
    email_id,
    subject,
    body,
    category,
    summary,
    deadline,
    relevance
):

    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO emails (
        email_id,
        subject,
        body,
        category,
        summary,
        deadline,
        relevance
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        email_id,
        subject,
        body,
        category,
        summary,
        deadline,
        relevance
    ))

    conn.commit()
    conn.close()