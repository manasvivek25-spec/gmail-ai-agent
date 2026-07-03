import sys
from database import get_db_connection
print('Connecting to DB...')
sys.stdout.flush()
try:
    conn = get_db_connection()
    print('Connected DB!')
    conn.close()
except Exception as e:
    print('DB Error:', e)
sys.stdout.flush()
from ai_agent import analyze_email
print('Testing Groq...')
sys.stdout.flush()
try:
    res = analyze_email('Test subject', 'Test body')
    print('Groq success:', res['category'])
except Exception as e:
    print('Groq Error:', e)
sys.stdout.flush()
