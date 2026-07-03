import sys
from email_memory import save_email
print('Saving email...')
sys.stdout.flush()
try:
    save_email('test_id', 'Subj', 'Body', 'ERROR', 'Error test', 'NONE', 0, 0, '2026-07-03T10:00:00Z', 'NONE')
    print('Saved successfully!')
except Exception as e:
    print('Save Error:', e)
sys.stdout.flush()
