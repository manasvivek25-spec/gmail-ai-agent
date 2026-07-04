import os, psycopg2
conn = psycopg2.connect(os.environ['SUPABASE_URL'])
cursor = conn.cursor()
cursor.execute('SELECT email_id, subject, substring(body from 1 for 100) FROM emails')
for row in cursor.fetchall():
    print(row)
conn.close()
