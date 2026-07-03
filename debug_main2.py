import sys
print('Starting debug2')
sys.stdout.flush()
from gmail_reader import get_latest_emails
print('Imported get_latest_emails')
sys.stdout.flush()
try:
    emails = get_latest_emails(2)
    print('Got emails!', len(emails))
except Exception as e:
    print('Error:', e)
sys.stdout.flush()
