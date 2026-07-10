import psycopg2
from database import get_db_connection

user_id = '107353106888683946567'
labels_to_restore = {
    'Internships': ['internship', 'intern', 'stipend', 'hackathon'],
    'Mess': ['mess menu', 'breakfast', 'lunch', 'dinner'],
    'Academic': ['academic', 'course', 'exam', 'assignment', 'nptel', 'phd']
}

try:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        for label, keywords in labels_to_restore.items():
            cursor.execute('INSERT INTO user_labels (user_id, label_name) VALUES (%s, %s) ON CONFLICT DO NOTHING', (user_id, label))
            for keyword in keywords:
                cursor.execute('INSERT INTO label_rules (user_id, label_name, keyword) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (user_id, label, keyword))
        conn.commit()
        print('Successfully restored custom labels and rules for the user!')
except Exception as e:
    print(e)

