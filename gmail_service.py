from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
from auth import CLIENT_ID, CLIENT_SECRET

def get_gmail_service(refresh_token):
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    
    if not creds.valid:
        creds.refresh(Request())

    service = build("gmail", "v1", credentials=creds)
    return service