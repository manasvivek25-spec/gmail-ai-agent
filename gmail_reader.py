from gmail_service import get_gmail_service
import base64

def get_email_body(payload):

    if 'parts' in payload:

        for part in payload['parts']:

            mime_type = part.get('mimeType')

            if mime_type in ['text/plain', 'text/html']:

                data = part['body'].get('data')

                if data:
                    return base64.urlsafe_b64decode(
                        data
                    ).decode(
                        'utf-8',
                        errors='ignore'
                    )

    data = payload.get('body', {}).get('data')

    if data:
        return base64.urlsafe_b64decode(
            data
        ).decode(
            'utf-8',
            errors='ignore'
        )

    return ""


def get_latest_emails(max_results=5):

    service = get_gmail_service()

    results = service.users().messages().list(
        userId='me',
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])

    emails = []

    for msg in messages:

        email = service.users().messages().get(
            userId='me',
            id=msg['id']
        ).execute()

        headers = email['payload']['headers']

        subject = "No Subject"

        sender = "Unknown"

        for header in headers:

            if header['name'] == 'Subject':
                subject = header['value']

            elif header['name'] == 'From':
                sender = header['value']

        body = get_email_body(
            email['payload']
        )

        emails.append({
            "id": msg["id"],
            "subject": subject,
            "sender": sender,
            "body": body
        })

    return emails