import re
with open('email_memory.py', 'r') as f:
    code = f.read()

# 1. Update function signatures to prepend user_id
code = re.sub(r'def ([a-zA-Z_]+)\((.*?)\):', r'def \1(user_id, \2):', code)
code = code.replace('(user_id, ):', '(user_id):')
code = code.replace('def calculate_importance(user_id, ', 'def calculate_importance(')

# 2. Fix SQL Queries
# emails table
code = code.replace('INSERT INTO emails (\n    email_id,', 'INSERT INTO emails (\n    user_id,\n    email_id,')
code = code.replace('VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
code = code.replace('ON CONFLICT (email_id)', 'ON CONFLICT (user_id, email_id)')
code = code.replace('(\n    email_id,\n    subject,', '(\n    user_id,\n    email_id,\n    subject,')

# 3. WHERE clauses
code = code.replace('WHERE email_id=%s', 'WHERE user_id=%s AND email_id=%s')
code = code.replace('(email_id,)', '(user_id, email_id)')

code = code.replace('WHERE label_name=%s', 'WHERE user_id=%s AND label_name=%s')
code = code.replace('(label_name,)', '(user_id, label_name)')

code = code.replace('WHERE category=%s', 'WHERE user_id=%s AND category=%s')
code = code.replace('(category,)', '(user_id, category)')

code = code.replace('WHERE name=%s', 'WHERE user_id=%s AND name=%s')
code = code.replace('(name,)', '(user_id, name)')

code = code.replace('WHERE interest=%s', 'WHERE user_id=%s AND interest=%s')
code = code.replace('(tag,)', '(user_id, tag)')

code = code.replace('WHERE e.email_id=%s', 'WHERE user_id=%s AND e.email_id=%s')

# 4. SELECT * without WHERE -> add WHERE user_id=%s
code = code.replace('FROM emails\n                ORDER BY', 'FROM emails\n                WHERE user_id=%s\n                ORDER BY')
code = code.replace('(limit,)', '(user_id, limit)')
code = code.replace('FROM emails\n            """,', 'FROM emails WHERE user_id=%s\n            """, (user_id,)')
code = code.replace('FROM user_labels"\n            )', 'FROM user_labels WHERE user_id=%s", (user_id,)')
code = code.replace('FROM emails GROUP BY', 'FROM emails WHERE user_id=%s GROUP BY')
code = code.replace('FROM email_tags GROUP BY tag ORDER BY count DESC LIMIT %s', 'FROM email_tags WHERE user_id=%s GROUP BY tag ORDER BY count DESC LIMIT %s')
code = code.replace('FROM user_interests ORDER BY score DESC LIMIT %s', 'FROM user_interests WHERE user_id=%s ORDER BY score DESC LIMIT %s')
code = code.replace('WHERE deadline !=', 'WHERE user_id=%s AND deadline !=')
code = code.replace('WHERE importance > 0', 'WHERE user_id=%s AND importance > 0')
code = code.replace('WHERE email_id = ANY(%s)', 'WHERE user_id=%s AND email_id = ANY(%s)')
code = code.replace('(email_ids,)', '(user_id, email_ids)')

# 5. INSERT / ON CONFLICT without emails
code = code.replace('INSERT INTO email_tags (email_id, tag) VALUES (%s, %s)', 'INSERT INTO email_tags (user_id, email_id, tag) VALUES (%s, %s, %s)')
code = code.replace('ON CONFLICT (email_id, tag)', 'ON CONFLICT (user_id, email_id, tag)')
code = code.replace('(email_id, tag)', '(user_id, email_id, tag)')

code = code.replace('INSERT INTO email_labels (email_id, label_name) VALUES (%s, %s)', 'INSERT INTO email_labels (user_id, email_id, label_name) VALUES (%s, %s, %s)')
code = code.replace('ON CONFLICT (email_id, label_name)', 'ON CONFLICT (user_id, email_id, label_name)')
code = code.replace('(email_id, label_name)', '(user_id, email_id, label_name)')

code = code.replace('INSERT INTO user_labels (label_name) VALUES (%s)', 'INSERT INTO user_labels (user_id, label_name) VALUES (%s, %s)')
code = code.replace('ON CONFLICT (label_name)', 'ON CONFLICT (user_id, label_name)')
code = code.replace('(label_name,)', '(user_id, label_name)')

code = code.replace('INSERT INTO label_rules (label_name, keyword) VALUES (%s, %s)', 'INSERT INTO label_rules (user_id, label_name, keyword) VALUES (%s, %s, %s)')
code = code.replace('ON CONFLICT (label_name, keyword)', 'ON CONFLICT (user_id, label_name, keyword)')
code = code.replace('(label_name, keyword)', '(user_id, label_name, keyword)')

code = code.replace('INSERT INTO user_actions (email_id, action_type) VALUES (%s, %s)', 'INSERT INTO user_actions (user_id, email_id, action_type) VALUES (%s, %s, %s)')
code = code.replace('(email_id, action_type)', '(user_id, email_id, action_type)')

code = code.replace('INSERT INTO user_interests (interest, score) VALUES (%s, %s)', 'INSERT INTO user_interests (user_id, interest, score) VALUES (%s, %s, %s)')
code = code.replace('ON CONFLICT (interest)', 'ON CONFLICT (user_id, interest)')
code = code.replace('(tag, score)', '(user_id, tag, score)')
code = code.replace('(score, tag)', '(score, user_id, tag)')

code = code.replace('UPDATE emails SET is_bookmarked', 'UPDATE emails SET is_bookmarked')
code = code.replace('(new_status, email_id)', '(new_status, user_id, email_id)')

# get_email_count tuple fix
code = code.replace('"""\n                SELECT COUNT(*) FROM emails\n                """\n            )', '"""\n                SELECT COUNT(*) FROM emails WHERE user_id=%s\n                """,\n                (user_id,)\n            )')

with open('email_memory.py', 'w') as f:
    f.write(code)
print('Rewritten successfully')
