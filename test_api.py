import urllib.request
req = urllib.request.Request('https://gmail-ai-agent-ih4e.onrender.com/api/emails')
req.add_header('Authorization', 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTA3MzUzMTA2ODg4NjgzOTQ2NTY3IiwiZXhwIjoxNzg1NzY4MDk5fQ.i8_dkqtCl4DPNWuxfHasaqoZ1CsfXqR3gkbPwJfsS-s')
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode('utf-8'))
except Exception as e:
    print(e)

