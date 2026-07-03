from database import get_db_connection
import psycopg2.extras

conn = get_db_connection()
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

cursor.execute("""
SELECT rowid,
       subject
FROM emails
ORDER BY rowid DESC
LIMIT 20
""")

for row in cursor.fetchall():
    print(row)

conn.close()