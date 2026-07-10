from database import get_db_connection
try:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO emails (user_id, email_id, subject)
    VALUES ('107353106888683946567', 'test_email', 'test')
    ON CONFLICT (user_id, email_id) DO UPDATE SET subject = 'test2'
    """)
    conn.commit()
    print("SUCCESS")
except Exception as e:
    print("ERROR:", e)
