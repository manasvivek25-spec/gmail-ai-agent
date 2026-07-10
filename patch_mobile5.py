import os
with open('mobile_app/lib/main.dart', 'r', encoding='utf-8') as f:
    code = f.read()

old_actions = '''        actions: [
          IconButton(
            icon: const Icon(Icons.refresh, color: Colors.white),
            onPressed: syncAgent,
          )
        ],'''

new_actions = '''        actions: [
          IconButton(
            icon: const Icon(Icons.logout, color: Colors.white),
            onPressed: () async {
              final prefs = await SharedPreferences.getInstance();
              await prefs.remove(\\'jwt_token\\');
              if (mounted) {
                Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => const LoginScreen()));
              }
            },
          ),
          IconButton(
            icon: const Icon(Icons.refresh, color: Colors.white),
            onPressed: syncAgent,
          )
        ],'''

code = code.replace(old_actions, new_actions)

with open('mobile_app/lib/main.dart', 'w', encoding='utf-8') as f:
    f.write(code)
print('Mobile app AppBar logout button added')

