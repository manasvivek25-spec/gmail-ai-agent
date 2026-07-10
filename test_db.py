import os
import psycopg2
from database import get_db_connection
with get_db_connection() as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, email FROM users')
    users = cursor.fetchall()
    print('USERS IN DB:', users)
    for u in users:
        cursor.execute('SELECT count(*) FROM emails WHERE user_id=%s', (u[0],))
        count = cursor.fetchone()[0]
        print(f'User {u[0]} has {count} emails')

