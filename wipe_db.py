import os, psycopg2
from dotenv import load_dotenv
load_dotenv()
conn = psycopg2.connect(os.environ['SUPABASE_URL'])
cursor = conn.cursor()
tables = ['emails', 'calendar_events', 'user_labels', 'label_rules', 'email_labels', 'email_tags', 'user_actions', 'user_interests']
for t in tables:
    cursor.execute(f'DROP TABLE IF EXISTS {t} CASCADE')
conn.commit()
print('Wiped old schema')
