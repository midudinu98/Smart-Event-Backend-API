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

from app.models.notification import NotificationType

from app.utils.security import require_role
from app.utils.notification import create_notification

from datetime import datetime, timezone
from app.models.coupon import Coupon

from sqlalchemy import update
from app.utils.connection_manager import manager

router = APIRouter(prefix="/bookings",tags=["Bookings"])

@router.post("/", response_model=BookingResponse)
async def create_booking(booking_data: BookingCreate,db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.USER, UserRole.ORGANIZER, UserRole.ADMIN))):
    # Step 1: Find the event
    event = db.query(Event).filter(Event.id == booking_data.event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if booking_data.ticket_quantity <= 0:
        raise HTTPException(status_code=400,detail="Ticket quantity must be greater than zero")
    
    # Step 2: Calculate original booking amount
    total_price = event.ticket_price * booking_data.ticket_quantity

    discount_amount = 0.0
    coupon_id = None

    # Step 3: Validate coupon if the user supplied one
    if booking_data.coupon_code:
        coupon = db.query(Coupon).filter(Coupon.coupon_code == booking_data.coupon_code.strip().upper()).first()

        if not coupon:
            raise HTTPException(status_code=404, detail="Coupon not found")

        if not coupon.is_active:
            raise HTTPException(status_code=400, detail="Coupon is inactive")

        now = datetime.now(timezone.utc)
        expiry = coupon.expiry_date

        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)

        if expiry <= now:
            raise HTTPException(status_code=400, detail="Coupon has expired")

        if coupon.used_count >= coupon.usage_limit:
            raise HTTPException(status_code=400,detail="Coupon usage limit reached")

        if total_price < coupon.minimum_booking_amount:
            raise HTTPException(status_code=400,detail="Booking amount is below the minimum required")

        # Step 4: Calculate discount
        discount_type = getattr(coupon.discount_type, "value", coupon.discount_type)

        if discount_type == "PERCENTAGE":
            discount_amount = total_price * coupon.discount_value / 100
        else:
            discount_amount = coupon.discount_value

        # Discount cannot exceed the original amount
        discount_amount = min(discount_amount, total_price)
        coupon_id = coupon.id

    # Step 5: Calculate final payable amount
    final_amount = round(total_price - discount_amount, 2)

    result = db.execute(update(Event).where(Event.id == booking_data.event_id,Event.available_tickets >= booking_data.ticket_quantity)
    .values(available_tickets=(Event.available_tickets - booking_data.ticket_quantity)))
    
    if result.rowcount == 0:
        db.rollback()
        raise HTTPException(status_code=400,detail="Not enough tickets available")

    # Step 6: Create booking
    booking = Booking(user_id=current_user.id,
        event_id=booking_data.event_id,
        ticket_quantity=booking_data.ticket_quantity,
        total_price=total_price,
        coupon_id=coupon_id,
        discount_amount=round(discount_amount, 2),
        final_amount=final_amount,
        booking_status="CONFIRMED")

    try:
        db.add(booking)
        db.flush()

        # Step 7: Generate ticket and QR code
        ticket_code = generate_ticket_code()
        qr_code_path = generate_qr_code(ticket_code)

        ticket = Ticket(booking_id=booking.id,
            ticket_code=ticket_code,
            qr_code_url=(
                f"http://127.0.0.1:8000/"
                f"{qr_code_path.replace(chr(92), '/')}"))
        db.add(ticket)

        # Step 8: Create booking confirmation notification
        create_notification(db=db,
            user_id=current_user.id,
            title="Booking Confirmed",
            message=f"Your booking for {event.title} has been confirmed.",
            notification_type=NotificationType.BOOKING,
            event_id=event.id)

        # Commit the inventory, booking, ticket, and notification
        db.commit()
        db.refresh(booking)

    except Exception:
        db.rollback()
        raise

    # Step 9: Broadcast updated availability after commit
    db.refresh(event)

    await manager.broadcast(
        event_id=event.id,
        message={"event_id": event.id,
            "available_tickets": event.available_tickets,
            "message": "Ticket availability updated"})

    return booking


@router.get("/my-bookings", response_model=list[BookingResponse])
def get_my_bookings(db: Session = Depends(get_db),current_user: User = Depends(
        require_role(UserRole.USER,UserRole.ORGANIZER,UserRole.ADMIN))):
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()
    return bookings