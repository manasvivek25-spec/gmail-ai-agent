import os, jwt, json
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from database import get_db_connection
import googleapiclient.discovery

router = APIRouter()
JWT_SECRET = os.environ.get('JWT_SECRET', 'super_secret_jwt_key_for_mail_agent')

CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

if "RENDER_EXTERNAL_URL" in os.environ:
    REDIRECT_URI = f"{os.environ['RENDER_EXTERNAL_URL']}/auth/google/callback"
else:
    REDIRECT_URI = "http://localhost:8000/auth/google/callback"
CLIENT_CONFIG = {
    'web': {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://oauth2.googleapis.com/token',
        'redirect_uris': [REDIRECT_URI]
    }
}
SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'openid', 'email', 'profile']

def get_current_user(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Missing or invalid token')
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')

@router.get('/auth/google/url')
def get_auth_url(platform: str = "web"):
    import urllib.parse
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
        "state": platform
    }
    auth_url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return {"url": auth_url}

@router.get('/auth/google/callback')
def auth_callback(code: str, state: str = "web"):
    import requests
    
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    r = requests.post(token_url, data=data)
    token_data = r.json()
    
    if "error" in token_data:
        raise HTTPException(status_code=400, detail=token_data)
        
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token", "")

    user_info = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers={'Authorization': f'Bearer {access_token}'}).json()
    user_id = user_info['id']
    email = user_info['email']

    with get_db_connection() as conn:
        cursor = conn.cursor()
        if refresh_token:
            cursor.execute(
                'INSERT INTO users (user_id, email, refresh_token) VALUES (%s, %s, %s) ON CONFLICT (user_id) DO UPDATE SET refresh_token = EXCLUDED.refresh_token',
                (user_id, email, refresh_token)
            )
        else:
            cursor.execute(
                'INSERT INTO users (user_id, email, refresh_token) VALUES (%s, %s, %s) ON CONFLICT (user_id) DO NOTHING',
                (user_id, email, "")
            )
        conn.commit()

    token = jwt.encode({'user_id': user_id}, JWT_SECRET, algorithm='HS256')
    
    if state == "mobile":
        from fastapi.responses import RedirectResponse
        return RedirectResponse(f"gmailaiagent://auth?token={token}")
        
    if state.startswith("http://") or state.startswith("https://") or state.startswith("tauri://"):
        from fastapi.responses import RedirectResponse
        return RedirectResponse(f"{state}/?token={token}")

    html = f"""
    <html>
        <head>
            <title>Login Successful</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #09090b; color: white; margin: 0; }}
                .container {{ background: #18181b; padding: 40px; border-radius: 24px; text-align: center; max-width: 500px; width: 90%; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); border: 1px solid #27272a; }}
                .token {{ background: #27272a; padding: 15px; border-radius: 12px; word-break: break-all; margin: 20px 0; color: #a1a1aa; font-family: monospace; font-size: 13px; border: 1px solid #3f3f46; }}
                button {{ background: #2563eb; color: white; border: none; padding: 12px 24px; border-radius: 12px; cursor: pointer; font-size: 15px; font-weight: 600; margin: 8px; transition: all 0.2s; }}
                button:hover {{ background: #1d4ed8; transform: translateY(-2px); }}
                button.secondary {{ background: #27272a; border: 1px solid #3f3f46; }}
                button.secondary:hover {{ background: #3f3f46; }}
                h1 {{ color: #60a5fa; margin-top: 0; }}
                .section {{ margin-top: 30px; padding-top: 25px; border-top: 1px solid #27272a; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Authentication Successful!</h1>
                <p style="color: #a1a1aa; font-size: 15px; line-height: 1.5;">You have successfully connected your Google account to Mail Agent.</p>
                
                <div class="section">
                    <h3 style="margin-bottom: 15px; color: #e4e4e7;">1. Web & Desktop App</h3>
                    <p style="color: #a1a1aa; font-size: 14px; margin-bottom: 20px;">Click below to securely route your token back to your dashboard.</p>
                    <button onclick="window.location.href='http://localhost:1420/?token={token}'">Open Tauri Desktop (1420)</button>
                    <button class="secondary" onclick="window.location.href='http://localhost:5173/?token={token}'">Open Web Browser (5173)</button>
                </div>
                
                <div class="section">
                    <h3 style="margin-bottom: 15px; color: #e4e4e7;">2. Mobile App</h3>
                    <p style="color: #a1a1aa; font-size: 14px;">Copy your Device Sync Token below and paste it into the Flutter mobile app.</p>
                    <div class="token" id="tokenBox">{token}</div>
                    <button class="secondary" onclick="navigator.clipboard.writeText(document.getElementById('tokenBox').innerText); alert('Token Copied Successfully!');">Copy Sync Token</button>
                </div>
            </div>
        </body>
    </html>
    """
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=html)

