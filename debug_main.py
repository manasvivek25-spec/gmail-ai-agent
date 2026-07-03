import sys
print('Starting debug')
sys.stdout.flush()
from gmail_service import get_gmail_service
print('Imported get_gmail_service')
sys.stdout.flush()
try:
    get_gmail_service()
    print('Got Gmail Service!')
except Exception as e:
    print('Gmail Error:', e)
sys.stdout.flush()
