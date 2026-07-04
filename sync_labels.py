import os, psycopg2
from dotenv import load_dotenv
from gmail_service import get_gmail_service
load_dotenv()
conn = psycopg2.connect(os.environ['SUPABASE_URL'])
cursor = conn.cursor()
service = get_gmail_service()
results = service.users().labels().list(userId='me').execute()
labels = results.get('labels', [])
system_labels = {'CHAT', 'SENT', 'INBOX', 'IMPORTANT', 'TRASH', 'DRAFT', 'SPAM', 'CATEGORY_FORUMS', 'CATEGORY_UPDATES', 'CATEGORY_PERSONAL', 'CATEGORY_PROMOTIONS', 'CATEGORY_SOCIAL', 'YELLOW_STAR', 'STARRED', 'UNREAD'}
for l in labels:
    name = l['name']
    if name not in system_labels:
        try:
            cursor.execute('INSERT INTO user_labels (label_name) VALUES (%s) ON CONFLICT (label_name) DO NOTHING', (name,))
            print(f'Synced label: {name}')
        except Exception as e:
            print(f'Error syncing {name}: {e}')
conn.commit()
conn.close()
print('Done syncing labels!')
