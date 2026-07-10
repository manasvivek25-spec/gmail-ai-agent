from database import get_db_connection

conn = get_db_connection()
cur = conn.cursor()
cur.execute("SELECT constraint_name, constraint_type FROM information_schema.table_constraints WHERE table_name = 'emails';")
print("Emails constraints:", cur.fetchall())

cur.execute("SELECT constraint_name, constraint_type FROM information_schema.table_constraints WHERE table_name = 'user_interests';")
print("Interests constraints:", cur.fetchall())

conn.close()
