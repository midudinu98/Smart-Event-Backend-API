
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.event_update import EventUpdate
from app.models.events import Event
from app.models.user import User, UserRole
from app.schemas.event_update import (
    EventUpdateCreate,
    EventUpdateResponse,
)
from app.utils.security import get_current_user

router = APIRouter(prefix="/event-updates",tags=["Event Updates"])


@router.post("/", response_model=EventUpdateResponse)
def create_event_update(data: EventUpdateCreate,db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),):
    
    if current_user.role not in (UserRole.ORGANIZER,UserRole.ADMIN):
        raise HTTPException(status_code=403,detail="Only organizers and admins can post updates")

    event = db.query(Event).filter(Event.id == data.event_id).first()

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")

    if (current_user.role == UserRole.ORGANIZER and event.organizer_id != current_user.id):
        raise HTTPException(status_code=403,detail="You can only update your own events")

    update = EventUpdate(event_id=data.event_id,message=data.message)

    db.add(update)
    db.commit()
    db.refresh(update)

    return update


@router.get("/{event_id}",response_model=list[EventUpdateResponse])
def get_event_updates(event_id: int,db: Session = Depends(get_db)):
    
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")

    return (db.query(EventUpdate).filter(EventUpdate.event_id == event_id)
        .order_by(EventUpdate.created_at.desc()).all())
