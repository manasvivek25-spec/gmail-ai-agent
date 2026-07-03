content = open('email_memory.py', 'r', encoding='utf-8').read()
content = content.replace('()', '()')
open('email_memory.py', 'w', encoding='utf-8').write(content)
print('Fixed email_memory.py!')
