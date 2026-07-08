import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:app_links/app_links.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:http/http.dart' as http;
import 'main.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  late AppLinks _appLinks;
  StreamSubscription<Uri>? _linkSubscription;

  @override
  void initState() {
    super.initState();
    _initDeepLinks();
  }

  void _initDeepLinks() {
    _appLinks = AppLinks();
    _linkSubscription = _appLinks.uriLinkStream.listen((uri) {
      if (uri.scheme == 'gmailaiagent' && uri.host == 'auth') {
        final token = uri.queryParameters['token'];
        if (token != null && token.isNotEmpty) {
          _handleSuccessfulLogin(token);
        }
      }
    });
  }

  void _handleSuccessfulLogin(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('jwt_token', token);
    
    if (mounted) {
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => const InboxScreen()),
      );
    }
  }

  @override
  void dispose() {
    _linkSubscription?.cancel();
    super.dispose();
  }

  void _launchGoogleSignIn() async {
    try {
      final response = await http.get(Uri.parse('https://gmail-ai-agent-ih4e.onrender.com/auth/google/url?platform=mobile'));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final urlStr = data['url'];
        if (urlStr != null) {
          final launched = await launchUrl(Uri.parse(urlStr));
          if (!launched) {
            throw Exception('Could not launch browser');
          }
        }
      } else {
        throw Exception('Server returned ${response.statusCode}');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error launching Google Sign-In: $e'),
            backgroundColor: Colors.red,
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF09090B),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                width: 100,
                height: 100,
                decoration: BoxDecoration(
                  color: Colors.blueAccent.withOpacity(0.1),
                  shape: BoxShape.circle,
                  border: Border.all(color: Colors.blueAccent.withOpacity(0.3), width: 2),
                ),
                child: const Icon(Icons.smart_toy, size: 50, color: Colors.blueAccent),
              ),
              const SizedBox(height: 32),
              const Text(
                "Mail Agent", 
                style: TextStyle(fontSize: 36, fontWeight: FontWeight.bold, color: Colors.white, letterSpacing: -1)
              ),
              const SizedBox(height: 16),
              const Text(
                "Your intelligent, multi-tenant AI email assistant. Sign in to seamlessly sync your inbox across all platforms.", 
                textAlign: TextAlign.center, 
                style: TextStyle(color: Colors.white70, fontSize: 14, height: 1.5)
              ),
              const SizedBox(height: 48),
              
              Material(
                color: Colors.white,
                borderRadius: BorderRadius.circular(30),
                elevation: 4,
                child: InkWell(
                  onTap: _launchGoogleSignIn,
                  borderRadius: BorderRadius.circular(30),
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(30),
                      border: Border.all(color: Colors.grey.shade300),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        // Custom Google G Logo using basic shapes/colors since we don't have the SVG asset
                        Container(
                          width: 24,
                          height: 24,
                          decoration: const BoxDecoration(
                            shape: BoxShape.circle,
                            color: Colors.white,
                          ),
                          child: const Center(
                            child: Text(
                              "G",
                              style: TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: Color(0xFF4285F4),
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(width: 16),
                        const Text(
                          "Continue with Google",
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                            color: Colors.black87,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 32),
              const Text(
                "By signing in, you agree to our Terms of Service and Privacy Policy.", 
                textAlign: TextAlign.center, 
                style: TextStyle(color: Colors.white30, fontSize: 12, height: 1.5)
              ),
            ],
          ),
        ),
      ),
    );
  }
}
