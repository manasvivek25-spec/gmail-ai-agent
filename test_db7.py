from database import get_db_connection

def test_upsert(query, params, name):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        print(f"SUCCESS: {name}")
    except Exception as e:
        print(f"ERROR on {name}: {e}")
    finally:
        conn.close()

user = None
test_upsert("INSERT INTO emails (user_id, email_id) VALUES (%s, 'test') ON CONFLICT (user_id, email_id) DO NOTHING", (user,), "emails")
test_upsert("INSERT INTO user_labels (user_id, label_name) VALUES (%s, 'test') ON CONFLICT (user_id, label_name) DO NOTHING", (user,), "user_labels")
test_upsert("INSERT INTO email_labels (user_id, email_id, label_name) VALUES (%s, 'test', 'test') ON CONFLICT (user_id, email_id, label_name) DO NOTHING", (user,), "email_labels")
test_upsert("INSERT INTO email_tags (user_id, email_id, tag) VALUES (%s, 'test', 'test') ON CONFLICT (user_id, email_id, tag) DO NOTHING", (user,), "email_tags")
test_upsert("INSERT INTO user_interests (user_id, keyword) VALUES (%s, 'test') ON CONFLICT (user_id, keyword) DO UPDATE SET score=1", (user,), "user_interests")
