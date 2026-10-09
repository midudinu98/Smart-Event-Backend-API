from datetime import datetime
from pydantic import BaseModel, Field

from app.models.events import EventStatus

class EventCreate(BaseModel):
    title: str = Field(min_length=3,max_length=150)
    description: str = Field(min_length=10)
    category: str
    location: str = Field(min_length=2,max_length=150)
    event_date: datetime
    end_date: datetime
    ticket_price: float = Field(gt=0)
    banner_image: str | None = None
    total_tickets: int = Field(gt=0)

class EventUpdate(BaseModel):
    title: str | None = Field(default=None,min_length=3,max_length=150)
    description: str | None = Field(default=None,min_length=10)
    category: str | None = None
    location: str | None = Field(default=None,min_length=2,max_length=150)
    event_date: datetime | None = None
    end_date: datetime | None = None
    ticket_price: float | None = Field(default=None,gt=0)
    banner_image: str | None = None    

class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    location: str
    event_date: datetime
    ticket_price: float
    banner_image: str | None
    total_tickets: int
    available_tickets: int
    organizer_id: int
    event_status: EventStatus
    created_at: datetime

    class Config:
        from_attributes = True