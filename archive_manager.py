def archive_email(service, message_id):

    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={
            "removeLabelIds": ["INBOX"]
        }
    ).execute()