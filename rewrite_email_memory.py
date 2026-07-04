import re
with open('email_memory.py', 'r') as f:
    content = f.read()

# Make sure all functions take user_id as first param (if not already)
funcs = re.findall(r'def ([a-zA-Z0-9_]+)\((.*?)\):', content)
for func_name, args in funcs:
    if func_name in ['calculate_importance']: continue
    args = args.strip()
    if not args.startswith('user_id'):
        if args == '':
            new_args = 'user_id'
        else:
            new_args = f'user_id, {args}'
        content = content.replace(f'def {func_name}({args}):', f'def {func_name}({new_args}):')

# We need to replace all SQL queries to include user_id
# For emails, user_labels, label_rules, email_labels, email_tags, user_actions, user_interests, calendar_events

# emails
content = content.replace('INSERT INTO emails (', 'INSERT INTO emails (user_id, ')
content = content.replace('VALUES (%s, ', 'VALUES (%s, %s, ')
content = content.replace('ON CONFLICT (email_id)', 'ON CONFLICT (user_id, email_id)')
content = content.replace('WHERE email_id=%s', 'WHERE user_id=%s AND email_id=%s')
content = content.replace('WHERE e.email_id=%s', 'WHERE e.user_id=%s AND e.email_id=%s')
content = content.replace('(email_id,', '(user_id, email_id,')

# user_labels
content = content.replace('INSERT INTO user_labels (', 'INSERT INTO user_labels (user_id, ')
content = content.replace('ON CONFLICT (label_name)', 'ON CONFLICT (user_id, label_name)')

# other simple where clauses
content = content.replace('WHERE name = %s', 'WHERE user_id=%s AND name = %s')
content = content.replace('WHERE label_name = %s', 'WHERE user_id=%s AND label_name = %s')
content = content.replace('WHERE tag = %s', 'WHERE user_id=%s AND tag = %s')

# For SELECT from emails without WHERE, add WHERE user_id=%s
content = re.sub(r'SELECT (.*?) FROM emails(.*?)ORDER', r'SELECT \1 FROM emails \2 WHERE user_id=%s ORDER', content, flags=re.DOTALL)

with open('email_memory.py', 'w') as f:
    f.write(content)
print('Rewritten')

