
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.events import Event
from app.models.booking import Booking
from app.utils.security import get_current_admin

from sqlalchemy import func,cast, Date


router = APIRouter(prefix="/admin/analytics",tags=["Admin Analytics"])

# Total registered users
@router.get("/total-users")
def get_total_users( db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    total_users = db.query(User).count()
    return {"total_users": total_users}

# Total events created
@router.get("/total-events")
def get_total_events(db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    total_events = db.query(Event).count()
    return {"total_events": total_events}

# Total tickets sold
@router.get("/total-tickets-sold")
def get_total_tickets_sold(db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    tickets_sold = (db.query(func.sum(Booking.ticket_quantity)).filter(Booking.booking_status == "CONFIRMED").scalar())
    return {"total_tickets_sold": tickets_sold or 0}

# Total bookings
@router.get("/total-bookings")
def get_total_bookings(db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    total_bookings = db.query(Booking).count()
    return {"total_bookings": total_bookings}

# Platform revenue summary
@router.get("/revenue-summary")
def get_revenue_summary(db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    
    total_revenue = (db.query(func.sum(Booking.total_price))
        .filter(Booking.booking_status == "CONFIRMED")
        .scalar())

    confirmed_bookings = (db.query(Booking).filter(Booking.booking_status == "CONFIRMED").count())

    return {"total_revenue": round(total_revenue or 0, 2),
        "confirmed_bookings": confirmed_bookings}

# Daily ticket sales
@router.get("/daily-ticket-sales")
def get_daily_ticket_sales(db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    
    results = (db.query(cast(Booking.created_at, Date).label("sale_date"),
            func.sum(Booking.ticket_quantity).label("tickets_sold"))
        .filter(Booking.booking_status == "CONFIRMED")
        .group_by(cast(Booking.created_at, Date))
        .order_by(cast(Booking.created_at, Date)).all())

    return [{"date": str(row.sale_date),
            "tickets_sold": row.tickets_sold}
        for row in results]


# Monthly booking trends
@router.get("/monthly-booking-trends")
def get_monthly_booking_trends(db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    month_column = func.strftime("%Y-%m", Booking.created_at)

    results = (db.query(month_column.label("month"),
            func.count(Booking.id).label("total_bookings"))
        .group_by(month_column).order_by(month_column).all())

    return [{"month": row.month,
            "total_bookings": row.total_bookings}
        for row in results]


# Most popular events
@router.get("/popular-events")
def get_popular_events(db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    
    results = (db.query(Event.id,Event.title,
            func.sum(Booking.ticket_quantity).label("tickets_sold"))
        .join(Booking, Booking.event_id == Event.id)
        .filter(Booking.booking_status == "CONFIRMED")
        .group_by(Event.id, Event.title)
        .order_by(func.sum(Booking.ticket_quantity).desc()).limit(10).all())

    return [{"event_id": row.id,
            "event_title": row.title,
            "tickets_sold": row.tickets_sold}
        for row in results]


# Top revenue-generating events
@router.get("/top-revenue-events")
def get_top_revenue_events(db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    
    results = (db.query(Event.id,Event.title,
            func.sum(Booking.total_price).label("total_revenue"))
        .join(Booking, Booking.event_id == Event.id)
        .filter(Booking.booking_status == "CONFIRMED")
        .group_by(Event.id, Event.title)
        .order_by(func.sum(Booking.total_price).desc()).limit(10).all())

    return [{"event_id": row.id,
            "event_title": row.title,
            "total_revenue": round(row.total_revenue or 0, 2)}
            for row in results]

# View all users
@router.get("/users")
def get_all_users(db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    
    users = db.query(User).all()

    return [{"id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at}
        for user in users]


# View all events
@router.get("/events")
def get_all_events(db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    
    events = db.query(Event).all()

    return [{"id": event.id,
            "title": event.title,
            "category": event.category,
            "location": event.location,
            "event_date": event.event_date,
            "ticket_price": event.ticket_price}
        for event in events]


# View all bookings
@router.get("/bookings")
def get_all_bookings(db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    
    bookings = db.query(Booking).all()

    return [{"id": booking.id,
            "user_id": booking.user_id,
            "event_id": booking.event_id,
            "ticket_quantity": booking.ticket_quantity,
            "total_price": booking.total_price,
            "booking_status": booking.booking_status,
            "created_at": booking.created_at}
        for booking in bookings]



