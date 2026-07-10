from database import get_db_connection

def test_full_save_email():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO emails (
            user_id, email_id, subject, body, category, summary, deadline, relevance, importance, received_time, adaptive_action
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id, email_id) DO UPDATE SET
            subject = EXCLUDED.subject,
            body = EXCLUDED.body,
            category = EXCLUDED.category,
            summary = EXCLUDED.summary,
            deadline = EXCLUDED.deadline,
            relevance = EXCLUDED.relevance,
            importance = EXCLUDED.importance,
            received_time = EXCLUDED.received_time,
            adaptive_action = EXCLUDED.adaptive_action
        """,
        (
            '107353106888683946567',
            'full_test_id',
            'test_sub',
            'test_body',
            'test_cat',
            'test_summary',
            '2024-01-01',
            0.5,
            1.0,
            123456789,
            'test_action'
        ))
        conn.commit()
        print("FULL SAVE SUCCESS")
    except Exception as e:
        print(f"FULL SAVE ERROR: {e}")

test_full_save_email()
