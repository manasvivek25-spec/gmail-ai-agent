import sys
from database import get_db_connection
from email_memory import get_all_labels, get_rules, assign_label

user_id = '107353106888683946567'

def retro_scan():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT email_id, subject, body FROM emails WHERE user_id=%s', (user_id,))
            emails = cursor.fetchall()
            
            print(f'Retro-scanning {len(emails)} emails against restored rules...')
            labels = get_all_labels(user_id)
            
            for email_id, subject, body in emails:
                text = (str(subject) + ' ' + str(body)).lower()
                for label in labels:
                    rules = get_rules(user_id, label)
                    for keyword in rules:
                        if keyword.lower() in text:
                            assign_label(user_id, email_id, label)
                            print(f'Assigned {label} to {email_id}')
                            break
    except Exception as e:
        print(e)

if __name__ == '__main__':
    retro_scan()

