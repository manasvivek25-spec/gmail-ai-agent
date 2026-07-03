import os
import psycopg2
os.environ['SUPABASE_URL'] = 'postgresql://postgres.lhcdowtxblorqakcvyly:ManasVivek25@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres'
conn = psycopg2.connect(os.environ['SUPABASE_URL'])
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM emails')
print('Count:', cursor.fetchone()[0])
