import psycopg2
from database import get_db_connection
try:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM emails WHERE category = 'Uncategorized'")
        conn.commit()
        print(f'Deleted {cursor.rowcount} uncategorized emails.')
except Exception as e:
    print(e)
