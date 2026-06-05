def get_or_create_label(service, label_name):

    labels = service.users().labels().list(
        userId='me'
    ).execute()

    for label in labels['labels']:

        if label['name'] == label_name:
            return label['id']

    label_object = {
        "name": label_name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show"
    }

    created = service.users().labels().create(
        userId='me',
        body=label_object
    ).execute()

    return created['id']
def apply_label(
    service,
    message_id,
    label_id
):

    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={
            "addLabelIds": [label_id]
        }
    ).execute()