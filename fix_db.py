import os, psycopg2
conn = psycopg2.connect(os.environ['SUPABASE_URL'])
cursor = conn.cursor()
cursor.execute('ALTER TABLE emails ALTER COLUMN received_time TYPE BIGINT')
conn.commit()
conn.close()
print('Fixed!')
