from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tickets import Ticket
from app.models.booking import Booking
from app.models.user import User,UserRole
from app.schemas.ticket import TicketResponse
from app.utils.security import require_role

router = APIRouter(prefix="/tickets",tags=["Tickets"])

@router.get("/my-tickets", response_model=list[TicketResponse])
def get_my_tickets(db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.USER,
            UserRole.ORGANIZER,
            UserRole.ADMIN))):
    tickets = (
        db.query(Ticket)
        .join(Booking, Ticket.booking_id == Booking.id)
        .filter(Booking.user_id == current_user.id)
        .all()
    )

    return tickets

@router.get("/verify/{ticket_code}")
def verify_ticket(ticket_code: str,db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_code == ticket_code).first()

    if not ticket:
        raise HTTPException(status_code=404,detail="Invalid ticket")

    return {
        "valid": True,
        "message": "Ticket is valid",
        "ticket_code": ticket.ticket_code,
        "booking_id": ticket.booking_id
    }