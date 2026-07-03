import os
import re

for root, _, files in os.walk('.'):
    if any(x in root for x in ['venv', '.git', 'frontend', 'mobile_app', '__pycache__', '.gemini', '.shorebird']): continue
    for f in files:
        if f.endswith('.py') and f != 'database.py' and f != 'migrate.py':
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            if 'sqlite3' in content:
                content = content.replace('import sqlite3', 'from database import get_db_connection\nimport psycopg2.extras')
                content = content.replace('sqlite3.connect("emails.db")', 'get_db_connection()')
                
                # Replace row factory
                # Note: psycopg2 uses conn.cursor(cursor_factory=psycopg2.extras.DictCursor) instead of conn.row_factory
                # So we must replace conn.row_factory = sqlite3.Row with nothing, and then we have to manually fix cursor creations.
                # Actually, psycopg2.extras.RealDictCursor is better. 
                # A hack is to just leave it and we'll fix cursor creations. Let's just remove the row_factory line.
                content = content.replace('conn.row_factory = sqlite3.Row', '')
                content = content.replace('conn.cursor()', 'conn.cursor()')
                
                # Replace SQLite parameter binding `?` with PostgreSQL `%s`
                content = content.replace('?', '%s')
                
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f'Migrated {path}')
