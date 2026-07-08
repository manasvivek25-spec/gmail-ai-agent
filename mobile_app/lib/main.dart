import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:io';
import 'package:workmanager/workmanager.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'login_screen.dart';
import 'login_screen.dart';

final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
    FlutterLocalNotificationsPlugin();

@pragma('vm:entry-point')
void callbackDispatcher() {
  Workmanager().executeTask((task, inputData) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('jwt_token') ?? '';
      final response = await http.get(
        Uri.parse('https://gmail-ai-agent-ih4e.onrender.com/api/emails'),
        headers: {'Bypass-Tunnel-Reminder': 'true', 'Authorization': 'Bearer $token'},
      );
      if (response.statusCode == 200) {
        final emails = json.decode(response.body) as List<dynamic>;
        if (emails.isNotEmpty) {
          final topEmail = emails.first;
          final emailId = topEmail['email_id'] ?? topEmail['id'];
          final priority = topEmail['priority']?.toString().toUpperCase() ?? 'LOW';
          
          final prefs = await SharedPreferences.getInstance();
          final lastNotifiedId = prefs.getString('last_notified_email_id');
          
          if (emailId != lastNotifiedId && (priority == 'CRITICAL' || priority == 'HIGH')) {
            await flutterLocalNotificationsPlugin.show(
              id: topEmail.hashCode,
              title: topEmail['subject'] ?? 'New Important Email',
              body: topEmail['summary'] ?? 'You have a new high priority email.',
              notificationDetails: const NotificationDetails(
                android: AndroidNotificationDetails(
                  'email_ai_channel',
                  'AI Assistant Notifications',
                  importance: Importance.max,
                  priority: Priority.high,
                  styleInformation: BigTextStyleInformation(''),
                ),
              ),
            );
            await prefs.setString('last_notified_email_id', emailId);
          }
        }
      }
    } catch (err) {
      print("Background fetch error: $err");
    }
    return Future.value(true);
  });
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  const AndroidInitializationSettings initializationSettingsAndroid =
      AndroidInitializationSettings('@mipmap/ic_launcher');
  const InitializationSettings initializationSettings =
      InitializationSettings(android: initializationSettingsAndroid);
  await flutterLocalNotificationsPlugin.initialize(settings: initializationSettings);
  
  await Workmanager().initialize(
    callbackDispatcher,
    isInDebugMode: false,
  );
  await Workmanager().registerPeriodicTask(
    "1",
    "emailSyncTask",
    frequency: const Duration(minutes: 15),
    constraints: Constraints(networkType: NetworkType.connected),
  );

  final prefs = await SharedPreferences.getInstance();
  final token = prefs.getString('jwt_token');

  runApp(EmailAIAgentApp(isAuthenticated: token != null && token.isNotEmpty));
}

class EmailAIAgentApp extends StatelessWidget {
  final bool isAuthenticated;
  const EmailAIAgentApp({super.key, required this.isAuthenticated});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mail Agent',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blueAccent),
        useMaterial3: true,
      ),
      home: isAuthenticated ? const InboxScreen() : const LoginScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class InboxScreen extends StatefulWidget {
  const InboxScreen({super.key});

  @override
  State<InboxScreen> createState() => _InboxScreenState();
}

class _InboxScreenState extends State<InboxScreen> {
  List<dynamic> emails = [];
  bool isLoading = true;
  String currentView = 'inbox'; // e.g., 'inbox', 'category:MESS', 'label:ProjectX'

  @override
  void initState() {
    super.initState();
    fetchEmails();
  }

  Future<void> fetchEmails() async {
    setState(() => isLoading = true);
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('jwt_token') ?? '';
      final response = await http.get(
        Uri.parse('https://gmail-ai-agent-ih4e.onrender.com/api/emails'),
        headers: {'Bypass-Tunnel-Reminder': 'true', 'Authorization': 'Bearer $token'},
      );
      if (response.statusCode == 200) {
        setState(() {
          emails = json.decode(response.body);
          isLoading = false;
        });
      } else if (response.statusCode == 401) {
        final prefs = await SharedPreferences.getInstance();
        await prefs.remove('jwt_token');
        if (mounted) {
          Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => const LoginScreen()));
        }
      } else {
        throw Exception('Failed to load emails');
      }
    } catch (e) {
      print('Error fetching emails: $e');
      setState(() => isLoading = false);
    }
  }

  Future<void> syncAgent() async {
    setState(() => isLoading = true);
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('jwt_token') ?? '';
      final response = await http.post(
        Uri.parse('https://gmail-ai-agent-ih4e.onrender.com/api/refresh'),
        headers: {'Bypass-Tunnel-Reminder': 'true', 'Authorization': 'Bearer $token'},
      );
      if (response.statusCode == 200) {
        // Sync completed, now fetch the updated emails
        await fetchEmails();
      } else if (response.statusCode == 401) {
        final prefs = await SharedPreferences.getInstance();
        await prefs.remove('jwt_token');
        if (mounted) {
          Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => const LoginScreen()));
        }
      } else {
        throw Exception('Failed to sync agent');
      }
    } catch (e) {
      print('Error syncing agent: $e');
      setState(() => isLoading = false);
    }
  }

  Future<void> createLabel(String name) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('jwt_token') ?? '';
      await http.post(
        Uri.parse('https://gmail-ai-agent-ih4e.onrender.com/api/labels/create'),
        headers: {
          'Content-Type': 'application/json',
          'Bypass-Tunnel-Reminder': 'true',
          'Authorization': 'Bearer $token'
        },
        body: json.encode({'name': name}),
      );
      fetchEmails();
    } catch (e) {
      print('Error creating label: $e');
    }
  }

  Future<void> createRule(String label, String keyword) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('jwt_token') ?? '';
      await http.post(
        Uri.parse('https://gmail-ai-agent-ih4e.onrender.com/api/rules/create'),
        headers: {
          'Content-Type': 'application/json',
          'Bypass-Tunnel-Reminder': 'true',
          'Authorization': 'Bearer $token'
        },
        body: json.encode({'label': label, 'keyword': keyword}),
      );
      fetchEmails();
    } catch (e) {
      print('Error creating rule: $e');
    }
  }

  void _showCreateLabelDialog() {
    String labelName = "";
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text("Create Label"),
          content: TextField(
            onChanged: (val) => labelName = val,
            decoration: const InputDecoration(hintText: "Enter new label name"),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text("Cancel"),
            ),
            ElevatedButton(
              onPressed: () {
                if (labelName.isNotEmpty) {
                  createLabel(labelName);
                  Navigator.pop(context);
                }
              },
              child: const Text("Create"),
            )
          ],
        );
      },
    );
  }

  void _showCreateRuleDialog() {
    String labelName = "";
    String keyword = "";
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text("Create Rule"),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                onChanged: (val) => labelName = val,
                decoration: const InputDecoration(hintText: "Existing label to assign to"),
              ),
              TextField(
                onChanged: (val) => keyword = val,
                decoration: const InputDecoration(hintText: "Keyword to route"),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text("Cancel"),
            ),
            ElevatedButton(
              onPressed: () {
                if (labelName.isNotEmpty && keyword.isNotEmpty) {
                  createRule(labelName, keyword);
                  Navigator.pop(context);
                }
              },
              child: const Text("Create"),
            )
          ],
        );
      },
    );
  }

  List<dynamic> get filteredEmails {
    if (currentView == 'inbox') return emails;
    if (currentView == 'recommended') {
      return emails.where((e) => (e['importance'] ?? 0) > 0).toList();
    }
    if (currentView == 'deadlines') {
      return emails.where((e) => e['deadline'] != null && e['deadline'] != 'NONE' && e['deadline'] != '').toList();
    }
    if (currentView.startsWith('category:')) {
      final category = currentView.split(':')[1];
      return emails.where((e) => e['category'] == category).toList();
    }
    if (currentView.startsWith('label:')) {
      final label = currentView.split(':')[1];
      return emails.where((e) {
        final labels = e['labels'] as List<dynamic>? ?? [];
        return labels.contains(label);
      }).toList();
    }
    return emails;
  }

  @override
  Widget build(BuildContext context) {
    // Extract unique categories and labels from emails
    final Map<String, int> categories = {};
    final Set<String> labels = {};
    for (var email in emails) {
      if (email['category'] != null) {
        categories[email['category']] = (categories[email['category']] ?? 0) + 1;
      }
      final eLabels = email['labels'] as List<dynamic>? ?? [];
      for (var l in eLabels) {
        labels.add(l.toString());
      }
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(currentView.toUpperCase(), style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white, fontSize: 16)),
        backgroundColor: Colors.blueAccent,
        iconTheme: const IconThemeData(color: Colors.white),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout, color: Colors.white),
            onPressed: () async {
              final prefs = await SharedPreferences.getInstance();
              await prefs.remove('jwt_token');
              if (mounted) {
                Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => const LoginScreen()));
              }
            },
          ),
          IconButton(
            icon: const Icon(Icons.refresh, color: Colors.white),
            onPressed: syncAgent,
          )
        ],
      ),
      drawer: Drawer(
        child: Column(
          children: [
            const UserAccountsDrawerHeader(
              decoration: BoxDecoration(color: Colors.blueAccent),
              accountName: Text("AI Email Agent", style: TextStyle(fontWeight: FontWeight.bold)),
              accountEmail: Text("Your Personal Inbox Assistant"),
            ),
            Expanded(
              child: ListView(
                padding: EdgeInsets.zero,
                children: [
                  ListTile(
                    leading: const Icon(Icons.inbox),
                    title: const Text('Inbox'),
                    onTap: () {
                      setState(() => currentView = 'inbox');
                      Navigator.pop(context);
                    },
                  ),
                  const Divider(),
                  const Padding(
                    padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    child: Text('SMART CATEGORIES', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.grey)),
                  ),
                  ListTile(
                    leading: const Icon(Icons.local_fire_department, size: 20),
                    title: const Text('Recommended'),
                    onTap: () {
                      setState(() => currentView = 'recommended');
                      Navigator.pop(context);
                    },
                  ),
                  ListTile(
                    leading: const Icon(Icons.calendar_today, size: 20),
                    title: const Text('Deadlines'),
                    onTap: () {
                      setState(() => currentView = 'deadlines');
                      Navigator.pop(context);
                    },
                  ),
                  ...categories.keys.map((cat) => ListTile(
                    leading: const Icon(Icons.folder_special, size: 20),
                    title: Text(cat),
                    trailing: Text(categories[cat].toString(), style: const TextStyle(color: Colors.grey)),
                    onTap: () {
                      setState(() => currentView = 'category:$cat');
                      Navigator.pop(context);
                    },
                  )),
                  if (labels.isNotEmpty) ...[
                    const Divider(),
                    const Padding(
                      padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      child: Text('CUSTOM LABELS', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.grey)),
                    ),
                    ...labels.map((lbl) => ListTile(
                      leading: const Icon(Icons.label, size: 20),
                      title: Text(lbl),
                      onTap: () {
                        setState(() => currentView = 'label:$lbl');
                        Navigator.pop(context);
                      },
                    )),
                  ],
                  ListTile(
                    leading: const Icon(Icons.settings),
                    title: const Text('Settings'),
                    onTap: () {
                      Navigator.pop(context);
                    },
                  ),
                  ListTile(
                    leading: const Icon(Icons.logout, color: Colors.red),
                    title: const Text('Sign Out', style: TextStyle(color: Colors.red)),
                    onTap: () async {
                      final prefs = await SharedPreferences.getInstance();
                      await prefs.remove('jwt_token');
                      Navigator.pushReplacement(
                        context,
                        MaterialPageRoute(builder: (context) => const LoginScreen()),
                      );
                    },
                  ),
                ],
              ),
            ),
            Container(
              padding: const EdgeInsets.all(16.0),
              child: SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  icon: const Icon(Icons.sync),
                  label: const Text('Sync Agent'),
                  onPressed: () {
                    Navigator.pop(context);
                    syncAgent();
                  },
                ),
              ),
            )
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Show bottom sheet with actions
          showModalBottomSheet(
            context: context,
            shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
            builder: (context) => Container(
              padding: const EdgeInsets.all(24),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text('Intelligent Actions', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 20),
                  ListTile(
                    leading: const CircleAvatar(backgroundColor: Colors.blueAccent, child: Icon(Icons.label, color: Colors.white)),
                    title: const Text('Create Label'),
                    onTap: () {
                      Navigator.pop(context);
                      _showCreateLabelDialog();
                    },
                  ),
                  ListTile(
                    leading: const CircleAvatar(backgroundColor: Colors.purpleAccent, child: Icon(Icons.rule, color: Colors.white)),
                    title: const Text('Create Rule'),
                    onTap: () {
                      Navigator.pop(context);
                      _showCreateRuleDialog();
                    },
                  ),
                ],
              ),
            ),
          );
        },
        backgroundColor: Colors.blueAccent,
        child: const Icon(Icons.auto_awesome, color: Colors.white),
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: syncAgent,
              child: ListView.builder(
                padding: const EdgeInsets.symmetric(vertical: 8),
                itemCount: filteredEmails.length,
                itemBuilder: (context, index) {
                  final email = filteredEmails[index];
                  final subject = email['subject'] ?? 'No Subject';
                  final firstLetter = subject.isNotEmpty ? subject[0].toUpperCase() : '?';
                  return Dismissible(
                    key: Key(email['email_id'] ?? index.toString()),
                    background: Container(
                      color: Colors.green,
                      alignment: Alignment.centerLeft,
                      padding: const EdgeInsets.only(left: 20),
                      child: const Icon(Icons.archive, color: Colors.white),
                    ),
                    secondaryBackground: Container(
                      color: Colors.red,
                      alignment: Alignment.centerRight,
                      padding: const EdgeInsets.only(right: 20),
                      child: const Icon(Icons.delete, color: Colors.white),
                    ),
                    onDismissed: (direction) {
                      setState(() {
                        filteredEmails.removeAt(index);
                      });
                    },
                    child: Card(
                      elevation: 0,
                      margin: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 4.0),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                        side: BorderSide(color: Colors.grey.shade200),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.symmetric(vertical: 8.0),
                        child: ListTile(
                          leading: CircleAvatar(
                            radius: 24,
                            backgroundColor: Colors.blue.shade50,
                            child: Text(firstLetter, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.blueAccent)),
                          ),
                          title: Text(subject, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const SizedBox(height: 6),
                              Text(
                                email['summary'] ?? '',
                                maxLines: 2,
                                overflow: TextOverflow.ellipsis,
                                style: TextStyle(color: Colors.grey.shade700, height: 1.3),
                              ),
                              const SizedBox(height: 12),
                              Row(
                                children: [
                                  Container(
                                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                    decoration: BoxDecoration(
                                      color: Colors.blue.shade50,
                                      borderRadius: BorderRadius.circular(12),
                                    ),
                                    child: Text(email['category'] ?? 'UNKNOWN', style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.blue.shade700)),
                                  ),
                                  const Spacer(),
                                  if (email['relevance'] != null)
                                    Row(
                                      children: [
                                        const Icon(Icons.local_fire_department, size: 14, color: Colors.orange),
                                        const SizedBox(width: 4),
                                        Text('${email['relevance']}', style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.orange)),
                                      ],
                                    ),
                                ],
                              )
                            ],
                          ),
                          isThreeLine: true,
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => EmailDetailScreen(email: email),
                              ),
                            );
                          },
                        ),
                      ),
                    ),
                  );
                },
              ),
          ),
    );
  }
}

class EmailDetailScreen extends StatefulWidget {
  final dynamic email;

  const EmailDetailScreen({super.key, required this.email});

  @override
  State<EmailDetailScreen> createState() => _EmailDetailScreenState();
}

class _EmailDetailScreenState extends State<EmailDetailScreen> {
  bool _showRawEmail = false;
  bool _isLoadingBody = true;
  String _fullBody = 'No body available.';
  String _fullDeadline = 'NONE';
  List<dynamic> _fullTags = [];
  List<dynamic> _fullLabels = [];

  @override
  void initState() {
    super.initState();
    _fetchFullEmail();
  }

  Future<void> _fetchFullEmail() async {
    try {
      final emailId = widget.email['email_id'] ?? widget.email['id'];
      if (emailId == null) return;
      
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('jwt_token') ?? '';
      final response = await http.get(
        Uri.parse('https://gmail-ai-agent-ih4e.onrender.com/api/emails/$emailId'),
        headers: {
          'Bypass-Tunnel-Reminder': 'true',
          'Authorization': 'Bearer $token'
        },
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (mounted) {
          setState(() {
            _fullBody = data['body'] ?? 'No body available.';
            _fullDeadline = data['deadline'] ?? 'NONE';
            _fullTags = data['tags'] ?? [];
            _fullLabels = data['labels'] ?? [];
            _isLoadingBody = false;
          });
        }
      } else {
        if (mounted) setState(() => _isLoadingBody = false);
      }
    } catch (e) {
      print('Error fetching full email: $e');
      if (mounted) setState(() => _isLoadingBody = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final email = widget.email;
    final labels = _fullLabels.isNotEmpty ? _fullLabels : (email['labels'] as List<dynamic>? ?? []);
    final tags = _fullTags.isNotEmpty ? _fullTags : (email['tags'] as List<dynamic>? ?? []);
    
    final subject = email['subject'] ?? 'No Subject';
    final firstLetter = subject.isNotEmpty ? subject[0].toUpperCase() : '?';

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text('', style: TextStyle(color: Colors.black87)),
        backgroundColor: Colors.white,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.black87),
        actions: [
          IconButton(icon: const Icon(Icons.archive_outlined), onPressed: () {}),
          IconButton(icon: const Icon(Icons.more_vert), onPressed: () {}),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                CircleAvatar(
                  radius: 24,
                  backgroundColor: Colors.blue.shade50,
                  child: Text(firstLetter, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.blueAccent)),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        subject,
                        style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, height: 1.2),
                      ),
                      const SizedBox(height: 6),
                      Text('Received: ${email['time'] ?? 'Unknown'}', style: const TextStyle(color: Colors.grey, fontSize: 12)),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(color: Colors.blue.shade50, borderRadius: BorderRadius.circular(16)),
                  child: Text(email['category'] ?? 'UNKNOWN', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.blue.shade700)),
                ),
                const SizedBox(width: 8),
                if (email['priority'] != null)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: email['priority'] == 'Critical' ? Colors.red.shade50 : (email['priority'] == 'High' ? Colors.orange.shade50 : Colors.green.shade50),
                      borderRadius: BorderRadius.circular(16)
                    ),
                    child: Text(email['priority'], style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: email['priority'] == 'Critical' ? Colors.red.shade700 : (email['priority'] == 'High' ? Colors.orange.shade700 : Colors.green.shade700))),
                  ),
                const Spacer(),
                if (email['relevance'] != null)
                  Row(
                    children: [
                      const Icon(Icons.local_fire_department, color: Colors.orange, size: 18),
                      const SizedBox(width: 4),
                      Text('${email['relevance']}/10 Relevance', style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.orange)),
                    ],
                  ),
              ],
            ),
            const SizedBox(height: 32),
            const Text('AI BRIEF', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.blueAccent, letterSpacing: 1.5)),
            const SizedBox(height: 12),
            Text(
              email['summary'] ?? 'No summary available.',
              style: const TextStyle(fontSize: 18, color: Colors.black87, height: 1.5, fontWeight: FontWeight.w500),
            ),
            
            if (_fullDeadline != 'NONE' && _fullDeadline.isNotEmpty) ...[
              const SizedBox(height: 24),
              const Text('DEADLINE', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.redAccent, letterSpacing: 1.5)),
              const SizedBox(height: 8),
              Row(
                children: [
                  const Icon(Icons.calendar_today, color: Colors.redAccent, size: 20),
                  const SizedBox(width: 8),
                  Text(_fullDeadline, style: const TextStyle(fontSize: 16, color: Colors.black87, fontWeight: FontWeight.w600)),
                ],
              ),
            ],
            
            if (labels.isNotEmpty || tags.isNotEmpty) ...[
              const SizedBox(height: 32),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: [
                  ...labels.map((l) => Chip(label: Text(l, style: const TextStyle(fontSize: 11)), backgroundColor: Colors.grey.shade100, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)))),
                  ...tags.map((t) => Chip(label: Text(t, style: const TextStyle(fontSize: 11)), backgroundColor: Colors.purple.shade50, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)))),
                ],
              ),
            ],
            
            const SizedBox(height: 40),
            Center(
              child: OutlinedButton.icon(
                onPressed: () {
                  setState(() {
                    _showRawEmail = !_showRawEmail;
                  });
                },
                icon: Icon(_showRawEmail ? Icons.visibility_off : Icons.visibility),
                label: Text(_showRawEmail ? 'Hide Original Mail' : 'Read Original Full Mail'),
                style: OutlinedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                ),
              ),
            ),
            
            if (_showRawEmail) ...[
              const SizedBox(height: 24),
              const Divider(),
              const SizedBox(height: 16),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.grey.shade50,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.grey.shade200)
                ),
                child: _isLoadingBody 
                  ? const Center(child: Padding(padding: EdgeInsets.all(20), child: CircularProgressIndicator()))
                  : Text(
                      _fullBody,
                      style: const TextStyle(fontSize: 14, height: 1.6, color: Colors.black87, fontFamily: 'monospace'),
                    ),
              ),
            ],
            const SizedBox(height: 40),
          ],
        ),
      ),
    );
  }
}
