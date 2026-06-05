from datetime import datetime

def create_event(
    service,
    title,
    date_string
):

    event = {
        "summary": title,

        "start": {
            "date": date_string
        },

        "end": {
            "date": date_string
        }
    }

    service.events().insert(
        calendarId='primary',
        body=event
    ).execute()

    print(
        f"Calendar Event Created: {title}"
    )