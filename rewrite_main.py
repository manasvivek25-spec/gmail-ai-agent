import re
with open('main.py', 'r') as f:
    content = f.read()

# Make functions take user_id
content = content.replace('def auto_assign_labels(', 'def auto_assign_labels(user_id, ')
content = content.replace('get_all_labels()', 'get_all_labels(user_id)')
content = content.replace('get_rules(label)', 'get_rules(user_id, label)')
content = content.replace('assign_label(', 'assign_label(user_id, ')

content = content.replace('def calculate_relevance(tags):', 'def calculate_relevance(user_id, tags):')
content = content.replace('get_interest_score(t)', 'get_interest_score(user_id, t)')

content = content.replace('def main():', '''def main():
    from database import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, refresh_token FROM users")
    users = cursor.fetchall()
    conn.close()
    for user_id, refresh_token in users:
        print(f"Processing user {user_id}...")
        process_user(user_id, refresh_token)

def process_user(user_id, refresh_token):''')

# Fix calls in process_user (which was main)
content = re.sub(r'service = get_gmail_service\(\)', r'service = get_gmail_service(refresh_token)', content)
content = re.sub(r'calendar_service = get_calendar_service\(\)', r'calendar_service = get_calendar_service(refresh_token)', content)
content = re.sub(r'email_exists\((.*?)\)', r'email_exists(user_id, \1)', content)
content = re.sub(r'save_email\((.*?)\)', r'save_email(user_id, \1)', content)
content = re.sub(r'save_tag\((.*?)\)', r'save_tag(user_id, \1)', content)
content = re.sub(r'auto_assign_labels\((.*?)\)', r'auto_assign_labels(user_id, \1)', content)
content = re.sub(r'calculate_relevance\((.*?)\)', r'calculate_relevance(user_id, \1)', content)

# We need to make calendar_memory take user_id
content = re.sub(r'event_exists\((.*?)\)', r'event_exists(user_id, \1)', content)
content = re.sub(r'save_event\((.*?)\)', r'save_event(user_id, \1)', content)

with open('main.py', 'w') as f:
    f.write(content)
print('Rewrote main.py')
