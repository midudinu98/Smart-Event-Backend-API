from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.events import Event
from app.models.booking import Booking
from app.schemas.analytics import EventAnalyticsResponse
from app.utils.security import require_role
from app.models.user import User, UserRole

router = APIRouter(prefix="/analytics",tags=["Analytics"])

@router.get("/my-events",response_model=list[EventAnalyticsResponse])
def get_my_event_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ORGANIZER))):
    events = db.query(Event).filter(Event.organizer_id == current_user.id).all()

    analytics = []

    for event in events:

        bookings = db.query(Booking).filter(Booking.event_id == event.id,Booking.booking_status == "CONFIRMED").all()

        total_tickets_sold = sum(booking.ticket_quantity for booking in bookings)

        booking_count = len(bookings)

        total_revenue = sum(booking.total_price for booking in bookings)

        remaining_tickets = event.available_tickets

        analytics.append(
            EventAnalyticsResponse(
                event_id=event.id,
                event_title=event.title,
                total_tickets_sold=total_tickets_sold,
                remaining_tickets=remaining_tickets,
                total_revenue=total_revenue,
                booking_count=booking_count
            )
        )

    return analytics