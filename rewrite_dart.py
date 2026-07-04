import re
with open('mobile_app/lib/main.dart', 'r') as f:
    content = f.read()

# Change entrypoint to check token
content = content.replace('import \'package:shared_preferences/shared_preferences.dart\';', 'import \'package:shared_preferences/shared_preferences.dart\';\nimport \'login_screen.dart\';')
content = content.replace('runApp(const OmniAgentApp());', '''final prefs = await SharedPreferences.getInstance();
  final token = prefs.getString('jwt_token');
  runApp(MaterialApp(
    title: 'Mail Agent',
    theme: ThemeData(primarySwatch: Colors.blue),
    home: token != null ? const OmniAgentApp() : const LoginScreen(),
  ));''')

# Make sure OmniAgentApp doesn't wrap in MaterialApp again (Wait, OmniAgentApp is currently a StatelessWidget returning MaterialApp)
# If OmniAgentApp returns MaterialApp, we can just change the home of that MaterialApp instead.
# Let's fix that:
content = content.replace('''return MaterialApp(
      title: 'Email AI Agent',''', '''final prefs = SharedPreferences.getInstance();
    return MaterialApp(
      title: 'Mail Agent',''')

with open('mobile_app/lib/main.dart', 'w') as f:
    f.write(content)
print('Dart main updated')

