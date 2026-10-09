from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.events import Event
from app.schemas.events import EventCreate, EventResponse,EventUpdate,EventStatus

from app.models.user import User, UserRole
from app.utils.security import require_role

from app.models.booking import Booking
from app.schemas.booking import BookingResponse

from app.utils.event_status import update_event_status

from app.models.notification import Notification

router = APIRouter(prefix="/events", tags=["Events"])


# Create event
@router.post("/", response_model=EventResponse, status_code=201)
def create_event(event_data: EventCreate,db: Session = Depends(get_db),
                 current_user: User = Depends(require_role(UserRole.ORGANIZER))):
    new_event = Event(
        title=event_data.title,
        description=event_data.description,
        category=event_data.category,
        location=event_data.location,
        event_date=event_data.event_date,
        ticket_price=event_data.ticket_price,
        banner_image=event_data.banner_image,
        total_tickets=event_data.total_tickets,
        available_tickets=event_data.total_tickets,
        organizer_id=current_user.id,
        event_status="ACTIVE"
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


@router.get("")
def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    for event in events:
        update_event_status(event)
    db.commit()
    return events

@router.get("/my-events/bookings", response_model=list[BookingResponse])
def get_my_event_bookings(db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ORGANIZER))):
    bookings = (db.query(Booking).join(Event, Booking.event_id == Event.id).filter(Event.organizer_id == current_user.id).all())
    return bookings


@router.patch("/{event_id}/cancel",response_model=EventResponse)
def cancel_event(event_id: int,db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ORGANIZER))):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")

    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=403,detail="You can only cancel your own events")

    event.status = EventStatus.CANCELLED

    # Find confirmed bookings
    bookings = db.query(Booking).filter(Booking.event_id == event.id,Booking.booking_status == "CONFIRMED").all()

    # Notify booked users
    for booking in bookings:
        notification = Notification(
            user_id=booking.user_id,
            event_id=event.id,
            message=f'Event "{event.title}" has been cancelled.',
            notification_type="CANCELLED")

        db.add(notification)

    db.commit()
    db.refresh(event)

    return event

# Get single event
@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int,db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")

    return event


@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: int,event_data: EventUpdate,db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ORGANIZER))):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")

    # Organizer can modify only their own events
    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=403,detail="You can only manage your own events")

    update_data = event_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(event, field, value)

    # Find users who booked this event
    bookings = db.query(Booking).filter(Booking.event_id == event.id,Booking.booking_status == "CONFIRMED").all()

    # Create notification for each booked user
    for booking in bookings:
        notification = Notification(
            user_id=booking.user_id,
            event_id=event.id,
            message=f'Event "{event.title}" has been updated. Please check the latest event details.',
            notification_type="UPDATED")

        db.add(notification)

    db.commit()
    db.refresh(event)

    return event

# Search events by title
@router.get("/search/title", response_model=list[EventResponse])
def search_events(title: str = Query(..., min_length=1),db: Session = Depends(get_db)):
    events = db.query(Event).filter(Event.title.ilike(f"%{title}%")).all()
    return events

# Events by category
@router.get("/category/{category}", response_model=list[EventResponse])
def get_events_by_category(category: str,db: Session = Depends(get_db)):
    events = db.query(Event).filter(Event.category.ilike(category)).all()
    return events

@router.get("/my-events", response_model=list[EventResponse])
def get_my_events(db: Session = Depends(get_db),
                  current_user: User = Depends(require_role(UserRole.ORGANIZER))):
    events = (db.query(Event).filter(Event.organizer_id == current_user.id).all())
    return events