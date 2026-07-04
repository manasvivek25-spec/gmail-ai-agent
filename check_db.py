import psycopg2
from database import get_db_connection
try:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT category, importance FROM emails LIMIT 10')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
except Exception as e:
    print(e)

