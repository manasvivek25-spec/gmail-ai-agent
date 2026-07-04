import re
with open('api.py', 'r') as f:
    content = f.read()

content = content.replace('from fastapi import FastAPI, HTTPException', 'from fastapi import FastAPI, HTTPException, Depends\nfrom auth import router as auth_router, get_current_user')
content = content.replace('app = FastAPI(lifespan=lifespan)', 'app = FastAPI(lifespan=lifespan)\napp.include_router(auth_router)')

endpoints = re.findall(r'@app\.(?:get|post)\(.*?\)\ndef (.*?)\((.*?)\):', content)
for func_name, args in endpoints:
    if 'get_logs' in func_name or 'auth' in func_name or 'get_emails_by_category' in func_name: 
        if args.strip() == '':
            new_args = 'user_id: str = Depends(get_current_user)'
        else:
            new_args = args + ', user_id: str = Depends(get_current_user)'
        content = content.replace(f'def {func_name}({args}):', f'def {func_name}({new_args}):')
        continue
    
    if args.strip() == '':
        new_args = 'user_id: str = Depends(get_current_user)'
    else:
        new_args = args + ', user_id: str = Depends(get_current_user)'
    content = content.replace(f'def {func_name}({args}):', f'def {func_name}({new_args}):')

content = re.sub(r'email_memory\.([a-zA-Z0-9_]+)\(', r'email_memory.\1(user_id, ', content)

# Fix the hardcoded SQL in starred
content = content.replace('cursor.execute("SELECT email_id FROM emails WHERE is_bookmarked = 1 ORDER BY received_time DESC")', 'cursor.execute("SELECT email_id FROM emails WHERE user_id=%s AND is_bookmarked = 1 ORDER BY received_time DESC", (user_id,))')

with open('api.py', 'w') as f:
    f.write(content)
print('Rewrote api.py')
