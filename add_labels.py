import psycopg2
from database import get_db_connection

labels = ['Important', 'College', 'Hackathon']

try:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users LIMIT 1')
        row = cursor.fetchone()
        if row:
            user_id = row[0]
            for label in labels:
                cursor.execute('INSERT INTO user_labels (user_id, label_name) VALUES (%s, %s) ON CONFLICT DO NOTHING', (user_id, label))
            conn.commit()
            print(f'Labels added for {user_id}')
        else:
            print('No users found')
except Exception as e:
    print(f'Error: {e}')

