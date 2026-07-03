content = open('automation_engine.py', 'r', encoding='utf-8').read()
content = content.replace('()', '()')
open('automation_engine.py', 'w', encoding='utf-8').write(content)
print('Fixed automation_engine.py!')
