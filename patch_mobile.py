import re
with open('mobile_app/lib/main.dart', 'r', encoding='utf-8') as f:
    code = f.read()

if 'import \'dart:io\';' not in code:
    code = code.replace('import \'dart:convert\';', 'import \'dart:convert\';\nimport \'dart:io\';')

# Create a helper function inside _InboxScreenState or globally?
# We'll just replace the URLs inline.

base_url_str = "Platform.isAndroid ? 'http://10.0.2.2:8000' : 'http://127.0.0.1:8000'"

# 1. callbackDispatcher
old_callback = '''    try {
      final response = await http.get(
        Uri.parse('https://gmail-ai-agent-ih4e.onrender.com/api/emails'),
        headers: {'Bypass-Tunnel-Reminder': 'true'},
      );'''
new_callback = '''    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('jwt_token') ?? '';
      final response = await http.get(
        Uri.parse('${BASE_URL}/api/emails'),
        headers: {'Bypass-Tunnel-Reminder': 'true', 'Authorization': 'Bearer $token'},
      );'''.replace('${BASE_URL}', '${' + base_url_str + '}')
code = code.replace(old_callback, new_callback)

# 2. fetchEmails
old_fetch = '''    try {
      final response = await http.get(
        Uri.parse('https://gmail-ai-agent-ih4e.onrender.com/api/emails'),
        headers: {'Bypass-Tunnel-Reminder': 'true'},
      );'''
new_fetch = '''    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('jwt_token') ?? '';
      final response = await http.get(
        Uri.parse('${BASE_URL}/api/emails'),
        headers: {'Bypass-Tunnel-Reminder': 'true', 'Authorization': 'Bearer $token'},
      );'''.replace('${BASE_URL}', '${' + base_url_str + '}')
code = code.replace(old_fetch, new_fetch)

# 3. syncAgent
old_sync = '''    try {
      final response = await http.post(
        Uri.parse('https://gmail-ai-agent-ih4e.onrender.com/api/refresh'),
        headers: {'Bypass-Tunnel-Reminder': 'true'},
      );'''
new_sync = '''    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('jwt_token') ?? '';
      final response = await http.post(
        Uri.parse('${BASE_URL}/api/refresh'),
        headers: {'Bypass-Tunnel-Reminder': 'true', 'Authorization': 'Bearer $token'},
      );'''.replace('${BASE_URL}', '${' + base_url_str + '}')
code = code.replace(old_sync, new_sync)

# 4. createLabel
old_create_label = '''    try {
      await http.post(
        Uri.parse('https://gmail-ai-agent-ih4e.onrender.com/api/labels/create'),
        headers: {
          'Content-Type': 'application/json',
          'Bypass-Tunnel-Reminder': 'true'
        },'''
new_create_label = '''    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('jwt_token') ?? '';
      await http.post(
        Uri.parse('${BASE_URL}/api/labels/create'),
        headers: {
          'Content-Type': 'application/json',
          'Bypass-Tunnel-Reminder': 'true',
          'Authorization': 'Bearer $token'
        },'''.replace('${BASE_URL}', '${' + base_url_str + '}')
code = code.replace(old_create_label, new_create_label)

# 5. createRule
old_create_rule = '''    try {
      await http.post(
        Uri.parse('https://gmail-ai-agent-ih4e.onrender.com/api/rules/create'),
        headers: {
          'Content-Type': 'application/json',
          'Bypass-Tunnel-Reminder': 'true'
        },'''
new_create_rule = '''    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('jwt_token') ?? '';
      await http.post(
        Uri.parse('${BASE_URL}/api/rules/create'),
        headers: {
          'Content-Type': 'application/json',
          'Bypass-Tunnel-Reminder': 'true',
          'Authorization': 'Bearer $token'
        },'''.replace('${BASE_URL}', '${' + base_url_str + '}')
code = code.replace(old_create_rule, new_create_rule)

with open('mobile_app/lib/main.dart', 'w', encoding='utf-8') as f:
    f.write(code)
print('Mobile network logic patched successfully')
