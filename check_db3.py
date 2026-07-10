from database import get_db_connection

conn = get_db_connection()
cur = conn.cursor()
cur.execute("""
    SELECT a.attname
    FROM   pg_index i
    JOIN   pg_attribute a ON a.attrelid = i.indrelid
                         AND a.attnum = ANY(i.indkey)
    WHERE  i.indrelid = 'emails'::regclass
    AND    i.indisprimary;
""")
print("Primary key columns for emails:", [row[0] for row in cur.fetchall()])

conn.close()
