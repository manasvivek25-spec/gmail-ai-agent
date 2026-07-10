import re
with open('mobile_app/lib/main.dart', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r"\$\{Platform\.isAndroid \? 'http://10\.0\.2\.2:8000' : 'http://127\.0\.0\.1:8000'\}"
code = re.sub(pattern, 'https://gmail-ai-agent-ih4e.onrender.com', code)

with open('mobile_app/lib/main.dart', 'w', encoding='utf-8') as f:
    f.write(code)
print('Mobile network logic updated to Render')
