from app.models.events import EventStatus,Event
from datetime import datetime

def get_event_status(event_date: datetime,end_date: datetime,current_time: datetime | None = None) -> EventStatus:

    if current_time is None:
        current_time = datetime.utcnow()

    if current_time < event_date:
        return EventStatus.UPCOMING

    if event_date <= current_time <= end_date:
        return EventStatus.ONGOING

    return EventStatus.COMPLETED

def update_event_status(event:Event) -> EventStatus:

    # Do not automatically change a cancelled event
    if event.status == EventStatus.CANCELLED:
        return event.status

    event.status = get_event_status(
        event.event_date,
        event.end_date
    )

    return event.status