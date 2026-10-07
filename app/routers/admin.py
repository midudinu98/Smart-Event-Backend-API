from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.events import Event
from app.models.booking import Booking
from app.models.tickets import Ticket
from app.utils.security import get_current_admin

from app.schemas.user import AdminUserResponse


router = APIRouter(prefix="/admin",tags=["Admin"])


@router.get("/dashboard")
def admin_dashboard(db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):

    total_users = db.query(User).count()
    total_events = db.query(Event).count()
    total_bookings = db.query(Booking).count()

    confirmed_bookings = db.query(Booking).filter(Booking.booking_status == "CONFIRMED").count()
    pending_bookings = db.query(Booking).filter(Booking.booking_status == "PENDING").count()
    cancelled_bookings = db.query(Booking).filter(Booking.booking_status == "CANCELLED").count()

    total_tickets = db.query(Ticket).count()
    total_revenue = 0

    confirmed_booking_list = db.query(Booking).filter(Booking.booking_status == "CONFIRMED").all()

    for booking in confirmed_booking_list:total_revenue += booking.total_price

    return {
        "total_users": total_users,
        "total_events": total_events,

        "booking_statistics": {
            "total_bookings": total_bookings,
            "confirmed_bookings": confirmed_bookings,
            "pending_bookings": pending_bookings,
            "cancelled_bookings": cancelled_bookings
        },

        "ticket_statistics": {
            "total_tickets": total_tickets
        },

        "revenue_statistics": {
            "total_revenue": total_revenue
        }
    }


@router.get("/bookings")
def get_all_bookings(db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    bookings = db.query(Booking).all()
    return bookings

@router.get("/users", response_model=list[AdminUserResponse])
def get_all_users(
    db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    users = db.query(User).all()
    return users

@router.get("/events")
def get_all_events(db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    events = db.query(Event).all()
    return events