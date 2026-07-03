
def get_or_create_label(
    service,
    label_name
):

    try:

        labels_result = (
            service.users()
            .labels()
            .list(userId="me")
            .execute()
        )

        labels = labels_result.get(
            "labels",
            []
        )

        for label in labels:

            if label["name"] == label_name:

                print(
                    f"Using existing label: {label_name}"
                )

                return label["id"]

        label_object = {

            "name": label_name,

            "labelListVisibility":
            "labelShow",

            "messageListVisibility":
            "show"
        }

        created = (
            service.users()
            .labels()
            .create(
                userId="me",
                body=label_object
            )
            .execute()
        )

        print(
            f"Created label: {label_name}"
        )

        return created["id"]

    except Exception as e:

        print(
            f"Label Error: {e}"
        )

        return None


def apply_label(
    service,
    message_id,
    label_id
):

    try:

        if label_id is None:
            return

        (
            service.users()
            .messages()
            .modify(
                userId="me",
                id=message_id,
                body={
                    "addLabelIds":
                    [label_id]
                }
            )
            .execute()
        )

        print(
            f"Label Applied: {label_id}"
        )

    except Exception as e:

        print(
            f"Apply Label Error: {e}"
        )
