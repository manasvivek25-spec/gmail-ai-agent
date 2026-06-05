from calendar_service import get_calendar_service
from calendar_manager import create_event

service = get_calendar_service()

create_event(
    service,
    "Amazon ML Summer School Deadline",
    "2026-06-14"
)