from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.events import Event
from app.models.notification import Notification


def create_event_reminders(db: Session):

    now = datetime.now()
    reminder_time = now + timedelta(days=1)

    bookings = (db.query(Booking)
        .join(Event, Booking.event_id == Event.id)
        .filter(Booking.booking_status == "CONFIRMED",
            Event.event_date <= reminder_time,
            Event.event_date >= now
        ).all())

    for booking in bookings:

        event = db.query(Event).filter(Event.id == booking.event_id).first()

        existing_notification = (db.query(Notification)
            .filter(Notification.user_id == booking.user_id,
                Notification.type == "EVENT",
                Notification.message.contains(event.title)
            ).first())

        if not existing_notification:

            notification = Notification(user_id=booking.user_id,
                title="Upcoming Event",
                message=f"Your event {event.title} is coming up soon.",
                type="EVENT",
                is_read=False
            )

            db.add(notification)

    db.commit()