import sqlite3

def event_exists(email_id):

    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT email_id
        FROM calendar_events
        WHERE email_id=?
        """,
        (email_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


def save_event(email_id, title):

    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE
        INTO calendar_events
        VALUES (?, ?)
        """,
        (email_id, title)
    )

    conn.commit()
    conn.close()