from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import os

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

import json

def get_calendar_service():

    creds = None

    token_json = os.environ.get("CALENDAR_TOKEN_JSON")
    if token_json:
        creds = Credentials.from_authorized_user_info(json.loads(token_json), SCOPES)
    elif os.path.exists("calendar_token.json"):

        creds = Credentials.from_authorized_user_file(
            "calendar_token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                if os.environ.get("RENDER"):
                    raise Exception(f"Google Token Expired. Please update CALENDAR_TOKEN_JSON on Render. Error: {e}")
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json",
                    SCOPES
                )
                creds = flow.run_local_server(port=0)

        else:
            if os.environ.get("RENDER"):
                raise Exception("Missing or invalid Google Token on Render. Please provide a valid CALENDAR_TOKEN_JSON.")
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        if not token_json:
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