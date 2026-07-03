from database import get_db_connection
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM emails')
print('Total emails in DB:', cursor.fetchone()[0])
