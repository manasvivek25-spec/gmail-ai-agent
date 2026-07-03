import os, glob
for file in glob.glob('**/*.py', recursive=True):
    if 'venv' in file or '.git' in file or 'mobile_app' in file: continue
    if file == 'fix_all_cursors.py': continue
    content = open(file, 'r', encoding='utf-8').read()
    if '(cursor_factory=psycopg2.extras.RealDictCursor)' in content:
        content = content.replace('(cursor_factory=psycopg2.extras.RealDictCursor)', '()')
        open(file, 'w', encoding='utf-8').write(content)
        print(f'Fixed {file}')
