import os
with open('auth.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("os.environ.get('GOOGLE_CLIENT_ID')", 'CLIENT_ID')
code = code.replace('os.environ.get("GOOGLE_CLIENT_ID")', 'CLIENT_ID')
code = code.replace("os.environ.get('GOOGLE_CLIENT_SECRET')", 'CLIENT_SECRET')
code = code.replace('os.environ.get("GOOGLE_CLIENT_SECRET")', 'CLIENT_SECRET')

redirect_logic = '''if "RENDER_EXTERNAL_URL" in os.environ:
    REDIRECT_URI = f"{os.environ['RENDER_EXTERNAL_URL']}/auth/google/callback"
else:
    REDIRECT_URI = "http://localhost:8000/auth/google/callback"'''

if 'REDIRECT_URI =' not in code:
    code = code.replace('CLIENT_SECRET = "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"', f'CLIENT_SECRET = "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"\n\n{redirect_logic}')

code = code.replace("'redirect_uris': ['http://localhost:8000/auth/google/callback']", "'redirect_uris': [REDIRECT_URI]")
code = code.replace('"redirect_uri": "http://localhost:8000/auth/google/callback"', '"redirect_uri": REDIRECT_URI')

with open('auth.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('auth.py patched successfully')
