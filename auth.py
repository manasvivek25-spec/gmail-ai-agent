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
def get_auth_url():
    import urllib.parse
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent"
    }
    auth_url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return {"url": auth_url}

@router.get('/auth/google/callback')
def auth_callback(code: str):
    import requests
    
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
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
        # If the user logs in again and doesn't get a new refresh token (Google only sends it on first login), keep the old one!
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
    return RedirectResponse(url=f'http://localhost:1420/?token={token}')

