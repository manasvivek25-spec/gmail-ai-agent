
from datetime import datetime


def create_event(
    service,
    title,
    date_string
):

    try:

        if (
            not date_string
            or
            date_string == "NONE"
        ):
            return

        # Validate YYYY-MM-DD format
        datetime.strptime(
            date_string,
            "%Y-%m-%d"
        )

        event = {

            "summary": title,

            "start": {
                "date": date_string
            },

            "end": {
                "date": date_string
            }
        }

        created_event = (
            service.events()
            .insert(
                calendarId="primary",
                body=event
            )
            .execute()
        )

        print(
            f"Calendar Event Created: {title}"
        )

        print(
            f"Event ID: {created_event['id']}"
        )

    except ValueError:

        print(
            f"Invalid Date Format: {date_string}"
        )

    except Exception as e:

        print(
            f"Calendar Creation Error: {e}"
        )

