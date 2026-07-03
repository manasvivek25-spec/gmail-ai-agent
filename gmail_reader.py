from gmail_service import get_gmail_service
from bs4 import BeautifulSoup
import base64


def get_email_body(payload):

    if "parts" in payload:

        for part in payload["parts"]:

            mime_type = part.get("mimeType", "")

            if mime_type == "text/plain":

                data = part.get(
                    "body",
                    {}
                ).get("data")

                if data:

                    return base64.urlsafe_b64decode(
                        data
                    ).decode(
                        "utf-8",
                        errors="ignore"
                    )

        for part in payload["parts"]:

            mime_type = part.get("mimeType", "")

            if mime_type == "text/html":

                data = part.get(
                    "body",
                    {}
                ).get("data")

                if data:

                    return base64.urlsafe_b64decode(
                        data
                    ).decode(
                        "utf-8",
                        errors="ignore"
                    )

    data = payload.get(
        "body",
        {}
    ).get("data")

    if data:

        return base64.urlsafe_b64decode(
            data
        ).decode(
            "utf-8",
            errors="ignore"
        )

    return ""


def get_latest_emails(max_results=50):

    service = get_gmail_service()

    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            maxResults=max_results
        )
        .execute()
    )

    messages = results.get(
        "messages",
        []
    )

    emails = []

    for msg in messages:

        email = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=msg["id"]
            )
            .execute()
        )

        headers = email["payload"].get(
            "headers",
            []
        )

        subject = "No Subject"
        sender = "Unknown"

        for header in headers:

            if header["name"] == "Subject":
                subject = header["value"]

            elif header["name"] == "From":
                sender = header["value"]

        body = get_email_body(
            email["payload"]
        )

        soup = BeautifulSoup(
            body,
            "html.parser"
        )

        body = soup.get_text(
            separator="\n",
            strip=True
        )

        timestamp = int(
            email.get(
                "internalDate",
                0
            )
        )

        emails.append({

            "id": msg["id"],

            "subject": subject,

            "sender": sender,

            "body": body,

            "timestamp": timestamp

        })

    # Sort newest first
    emails.sort(
        key=lambda x: x["timestamp"],
        reverse=True
    )

    return emails