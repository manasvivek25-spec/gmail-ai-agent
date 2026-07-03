import requests
try:
    r = requests.get('https://gmail-ai-agent-ih4e.onrender.com/api/emails', timeout=15)
    print('Status:', r.status_code)
    print('Response:', r.text[:200])
except Exception as e:
    print('Error:', e)
