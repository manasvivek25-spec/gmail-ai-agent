import os
with open('mobile_app/lib/main.dart', 'r', encoding='utf-8') as f:
    code = f.read()

# We need to replace the error throwing in syncAgent
old_sync_error = '''      } else {
        throw Exception('Failed to sync agent');
      }'''

new_sync_error = '''      } else if (response.statusCode == 401) {
        final prefs = await SharedPreferences.getInstance();
        await prefs.remove('jwt_token');
        if (mounted) {
          Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => const LoginScreen()));
        }
      } else {
        throw Exception('Failed to sync agent');
      }'''

code = code.replace(old_sync_error, new_sync_error)

with open('mobile_app/lib/main.dart', 'w', encoding='utf-8') as f:
    f.write(code)
print('Mobile app 401 kickout logic updated for syncAgent')

