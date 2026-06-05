from gmail_service import get_gmail_service
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/calendar'
]

def get_calendar_service():

    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        SCOPES
    )

    creds = flow.run_local_server(port=0)

    service = build(
        'calendar',
        'v3',
        credentials=creds
    )

    return service