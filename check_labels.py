import psycopg2
from database import get_db_connection

try:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_labels')
        print('USER LABELS:', cursor.fetchall())
        cursor.execute('SELECT * FROM label_rules')
        print('LABEL RULES:', cursor.fetchall())
except Exception as e:
    print(e)

