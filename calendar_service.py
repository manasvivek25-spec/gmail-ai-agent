from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import os

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

def get_calendar_service():

    creds = None

    if os.path.exists("calendar_token.json"):

        creds = Credentials.from_authorized_user_file(
            "calendar_token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json",
                    SCOPES
                )
                creds = flow.run_local_server(port=0)

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open(
            "calendar_token.json",
            "w"
        ) as token:

            token.write(
                creds.to_json()
            )

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    return service