from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User,UserRole

from app.database import get_db
from app.models.booking import Booking
from app.models.events import Event
from app.schemas.booking import BookingCreate, BookingResponse

from app.models.tickets import Ticket
from app.utils.ticket import generate_ticket_code
from app.utils.qr_code import generate_qr_code

from app.models.notification import Notification

from app.utils.security import require_role

router = APIRouter(prefix="/bookings",tags=["Bookings"])

@router.post("/", response_model=BookingResponse)
def create_booking(booking_data: BookingCreate,db: Session = Depends(get_db), current_user: User =Depends(require_role(UserRole.USER, UserRole.ORGANIZER, UserRole.ADMIN))):
    event = db.query(Event).filter(Event.id == booking_data.event_id).first()

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")

    if event.available_tickets <= 0:
        raise HTTPException(status_code=400,detail="Tickets are sold out")
    
    if event.available_tickets < booking_data.ticket_quantity:
        raise HTTPException(status_code=400,detail="Not enough tickets available")

    total_price = event.price * booking_data.ticket_quantity

    booking = Booking(
        user_id=current_user.id,
        event_id=booking_data.event_id,
        ticket_quantity=booking_data.ticket_quantity,
        total_price=total_price,
        booking_status="CONFIRMED"
    )

    event.available_tickets -= booking_data.ticket_quantity

    db.add(booking)
    db.commit()
    db.refresh(booking)

    ticket_code = generate_ticket_code()

    qr_code_path = generate_qr_code(ticket_code)

    ticket = Ticket(booking_id=booking.id,ticket_code=ticket_code,qr_code_url=f"http://127.0.0.1:8000/{qr_code_path.replace(chr(92), '/')}")

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    notification = Notification(
    user_id=current_user.id,
    title="Booking Confirmed",
    message=f"Your booking for {event.title} has been confirmed.",
    type="BOOKING",
    is_read=False)

    db.add(notification)
    db.commit()

    return booking

@router.get("/my-bookings", response_model=list[BookingResponse])
def get_my_bookings(db: Session = Depends(get_db),current_user: User = Depends(
        require_role(UserRole.USER,UserRole.ORGANIZER,UserRole.ADMIN))):
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()
    return bookings