
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
import random

from app.database import get_db
from app.models.payment import Payment
from app.models.booking import Booking
from app.models.user import User
from app.schemas.payment import PaymentResponse
from app.utils.security import get_current_user

from app.utils.notification import create_notification
from app.models.notification import NotificationType

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/{booking_id}", response_model=PaymentResponse)
def make_payment(booking_id: int,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    # Find the booking
    booking = db.query(Booking).filter(Booking.id == booking_id,
        Booking.user_id == current_user.id).first()

    if not booking:
        raise HTTPException(status_code=404,detail="Booking not found")

    # Prevent payment for cancelled bookings
    if booking.status == "CANCELLED":
        raise HTTPException(status_code=400,detail="Cannot pay for a cancelled booking")

    # Prevent duplicate successful payments
    existing_payment = db.query(Payment).filter(Payment.booking_id == booking_id,
        Payment.payment_status == "SUCCESS").first()
    
    if existing_payment:
        raise HTTPException(status_code=400,detail="Booking has already been paid")

    # Create a pending payment record
    payment = Payment(booking_id=booking.id,
        payment_method="SIMULATED",
        payment_status="PENDING",
        amount=booking.total_price)

    db.add(payment)
    db.flush()

    
# Simulate the payment result
    payment_success = random.choice([True, False])

    if payment_success:
        payment.payment_status = "SUCCESS"
        payment.transaction_id = f"TXN-{uuid4().hex[:12].upper()}"
        booking.status = "CONFIRMED"

        notification_title = "Payment Successful"
        notification_message = (f"Your payment of ₹{payment.amount} "
        f"for booking ID {payment.booking_id} was successful.")

    else:
        payment.payment_status = "FAILED"

        notification_title = "Payment Failed"
        notification_message = (f"Your payment for booking ID "
        f"{payment.booking_id} failed. Please try again.")
    
    db.commit()
    db.refresh(payment)

# Create a notification for the actual payment result
    create_notification(db=db,
    user_id=current_user.id,
    title=notification_title,
    message=notification_message,
    notification_type=NotificationType.PAYMENT,)

    return payment


@router.get("/{booking_id}", response_model=list[PaymentResponse])
def get_booking_payments(booking_id: int,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    # Verify that the booking belongs to the logged-in user
    booking = db.query(Booking).filter(Booking.id == booking_id,
        Booking.user_id == current_user.id).first()

    if not booking:
        raise HTTPException(status_code=404,detail="Booking not found")

    return db.query(Payment).filter(Payment.booking_id == booking_id).all()
