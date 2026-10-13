from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.events import Event
from app.schemas.events import EventCreate, EventResponse,EventUpdate,EventStatus

from app.models.user import User, UserRole
from app.utils.security import require_role

from app.models.booking import Booking
from app.schemas.booking import BookingResponse

from app.utils.event_status import update_event_status

from app.models.notification import NotificationType
from app.utils.notification import create_notification

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
    
    event.status = EventStatus.CANCELLED

    # Find confirmed bookings
    bookings = (db.query(Booking).filter(Booking.event_id == event.id,Booking.booking_status == "CONFIRMED").all())

# Save event status before creating notifications
    db.commit()
    db.refresh(event)

# Notify booked users
    for booking in bookings:
           create_notification(db=db,
        user_id=booking.user_id,
        title="Event Cancelled",
        message=f'Event "{event.title}" has been cancelled.',
        notification_type=NotificationType.EVENT,
        event_id=event.id)

    return event


# Get single event
@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int,db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")

    return event



@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: int,event_data: EventUpdate,
    db: Session = Depends(get_db),current_user: User = Depends(require_role(UserRole.ORGANIZER))):
    
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")

    # Organizer can modify only their own events
    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=403,detail="You can only manage your own events")

    # Update event fields
    update_data = event_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(event, field, value)

    # Save event updates
    db.commit()
    db.refresh(event)

    # Find users with confirmed bookings
    bookings = (db.query(Booking).filter(Booking.event_id == event.id,
            Booking.booking_status == "CONFIRMED").all())

    # Notify every booked user
    for booking in bookings:
        create_notification(db=db,
            user_id=booking.user_id,
            title="Event Updated",
            message=(f'Event "{event.title}" has been updated. '
                "Please check the latest event details."),
            notification_type=NotificationType.EVENT,
            event_id=event.id)

    return event

# Search events by title
@router.get("/search")
def search_events(
    name: str | None = Query(default=None),
    category: str | None = Query(default=None),
    location: str | None = Query(default=None),
    start_date: datetime | None = Query(default=None),
    end_date: datetime | None = Query(default=None),
    db: Session = Depends(get_db),):

    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400,detail="Start date cannot be later than end date")
    
    query = db.query(Event)

    if name and name.strip():
        query = query.filter(Event.title.ilike(f"%{name.strip()}%"))

    if category and category.strip():
        query = query.filter(Event.category.ilike(f"%{category.strip()}%"))

    if location and location.strip():
        query = query.filter(Event.location.ilike(f"%{location.strip()}%"))

    if start_date:
        query = query.filter(Event.event_date >= start_date)

    if end_date:
        query = query.filter(Event.event_date <= end_date)

    return query.order_by(Event.event_date.asc()).all()


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