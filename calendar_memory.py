
from database import get_db_connection
import psycopg2.extras


def event_exists(email_id):

    try:

        with get_db_connection() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT email_id
                FROM calendar_events
                WHERE email_id=%s
                """,
                (email_id,)
            )

            result = cursor.fetchone()

            return result is not None

    except Exception as e:

        print(
            f"Calendar Memory Error: {e}"
        )

        return False


def save_event(email_id, title):

    try:

        with get_db_connection() as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO calendar_events (email_id, event_name)
                VALUES (%s, %s)
                ON CONFLICT (email_id) DO UPDATE SET
                    event_name = EXCLUDED.event_name
                """,
                (
                    email_id,
                    title
                )
            )

            conn.commit()

            print(
                f"CALENDAR EVENT SAVED: {title}"
            )

    except Exception as e:

        print(
            f"Calendar Save Error: {e}"
        )


def get_event_count():

    try:

        with get_db_connection() as conn:

            cursor = conn.cursor()

            cursor.execute("""
            SELECT COUNT(*)
            FROM calendar_events
            """)

            count = cursor.fetchone()[0]

            return count

    except Exception as e:

        print(
            f"Calendar Count Error: {e}"
        )

        return 0

