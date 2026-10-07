from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.events import Event
from app.schemas.events import EventCreate, EventResponse

from app.utils.security import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/events",tags=["Events"])

@router.post("/",response_model=EventResponse,status_code=201)
def create_event(event_data: EventCreate,db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    new_event = Event(
        title=event_data.title,
        description=event_data.description,
        category=event_data.category,
        location=event_data.location,
        event_date=event_data.event_date,
        ticket_price=event_data.ticket_price,
        banner_image=event_data.banner_image,
        total_tickets=event_data.total_tickets,
        available_tickets=event_data.total_tickets)

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

@router.get( "/", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events

@router.get("/{event_id}",response_model=EventResponse)
def get_event(event_id: int,db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")

    return event

@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: int,event_data: EventCreate,db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")

    event.title = event_data.title
    event.description = event_data.description
    event.category = event_data.category
    event.location = event_data.location
    event.event_date = event_data.event_date
    event.ticket_price = event_data.ticket_price
    event.banner_image = event_data.banner_image
    event.total_tickets = event_data.total_tickets
    event.available_tickets = event_data.total_tickets

    db.commit()
    db.refresh(event)

    return event

@router.delete("/{event_id}")
def delete_event(event_id: int,db: Session = Depends(get_db),current_admin: User = Depends(get_current_admin)):
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")

    db.delete(event)
    db.commit()

    return {"message": "Event deleted successfully"}

@router.get("/search/title",response_model=list[EventResponse])
def search_events(title: str = Query(..., min_length=1),db: Session = Depends(get_db)):
    events = db.query(Event).filter(Event.title.ilike(f"%{title}%")).all()
    return events

@router.get("/category/{category}",response_model=list[EventResponse])
def get_events_by_category(
    category: str,db: Session = Depends(get_db)):
    events = db.query(Event).filter(Event.category.ilike(category)).all()
    return events