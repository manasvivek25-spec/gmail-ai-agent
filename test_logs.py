import requests, sys
sys.stdout.reconfigure(encoding='utf-8')
print(requests.get('https://gmail-ai-agent-ih4e.onrender.com/api/logs', timeout=10).json().get('logs'))
