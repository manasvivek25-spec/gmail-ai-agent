from database import get_db_connection

def get_pk_columns(table):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT a.attname
        FROM   pg_index i
        JOIN   pg_attribute a ON a.attrelid = i.indrelid
                             AND a.attnum = ANY(i.indkey)
        WHERE  i.indrelid = '{table}'::regclass
        AND    i.indisprimary;
    """)
    cols = [row[0] for row in cur.fetchall()]
    conn.close()
    return cols

def get_unique_columns(table):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT a.attname
        FROM   pg_index i
        JOIN   pg_attribute a ON a.attrelid = i.indrelid
                             AND a.attnum = ANY(i.indkey)
        WHERE  i.indrelid = '{table}'::regclass
        AND    i.indisunique AND NOT i.indisprimary;
    """)
    cols = [row[0] for row in cur.fetchall()]
    conn.close()
    return cols

print("user_labels PK:", get_pk_columns('user_labels'), "UNIQUE:", get_unique_columns('user_labels'))
print("email_labels PK:", get_pk_columns('email_labels'))
print("email_tags PK:", get_pk_columns('email_tags'))
print("user_interests PK:", get_pk_columns('user_interests'))
