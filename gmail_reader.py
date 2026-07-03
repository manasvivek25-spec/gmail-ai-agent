from gmail_service import get_gmail_service
from bs4 import BeautifulSoup
import base64


def get_email_body(payload):
    def extract_data(payload_part):
        mime_type = payload_part.get("mimeType", "")
        if mime_type == "text/plain":
            data = payload_part.get("body", {}).get("data")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
        if "parts" in payload_part:
            for part in payload_part["parts"]:
                result = extract_data(part)
                if result:
                    return result
        return None

    # Try to find text/plain or text/html recursively
    result = extract_data(payload)
    if result:
        return result

    # Fallback to text/html recursively
    def extract_html(payload_part):
        mime_type = payload_part.get("mimeType", "")
        if mime_type == "text/html":
            data = payload_part.get("body", {}).get("data")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
        if "parts" in payload_part:
            for part in payload_part["parts"]:
                res = extract_html(part)
                if res:
                    return res
        return None

    res = extract_html(payload)
    if res:
        return res

    data = payload.get("body", {}).get("data")
    if data:
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

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