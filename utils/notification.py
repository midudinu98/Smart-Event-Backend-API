from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.events import Event
from app.models.notification import Notification, NotificationType

def create_event_reminders(db: Session):
    now = datetime.now()
    reminder_time = now + timedelta(days=1)

    bookings = (db.query(Booking).join(Event, Booking.event_id == Event.id)
        .filter(Booking.booking_status == "CONFIRMED",
            Event.event_date >= now,
            Event.event_date <= reminder_time).all())

    for booking in bookings:
        event = db.query(Event).filter(Event.id == booking.event_id).first()

        if event is None:
            continue

        existing_notification = (db.query(Notification)
            .filter(Notification.user_id == booking.user_id,
                Notification.event_id == event.id,
                Notification.notification_type == NotificationType.EVENT,
                Notification.title == "Upcoming Event").first())

        if not existing_notification:
            notification = Notification(user_id=booking.user_id,
                event_id=event.id,
                title="Upcoming Event",
                message=f"Your event {event.title} is coming up soon.",
                notification_type=NotificationType.EVENT,
                is_read=False)
            db.add(notification)
    db.commit()

def create_notification(db,
    user_id: int,
    title: str,
    message: str,
    notification_type: NotificationType,
    event_id: int | None = None):
    
    notification = Notification(user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
        event_id=event_id,
        is_read=False)

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification
