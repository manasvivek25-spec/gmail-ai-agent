import requests, time
for _ in range(10):
    r = requests.get('https://gmail-ai-agent-ih4e.onrender.com/api/logs', timeout=5)
    if r.status_code == 200:
        print(r.text)
        break
    time.sleep(10)
else: print('Timeout waiting for deployment')
