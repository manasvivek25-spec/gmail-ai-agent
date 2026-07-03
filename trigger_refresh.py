import requests
r = requests.post('https://gmail-ai-agent-ih4e.onrender.com/api/refresh', timeout=60)
print(r.json())
