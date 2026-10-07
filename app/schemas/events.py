from datetime import datetime
from pydantic import BaseModel, Field

class EventCreate(BaseModel):
    title: str = Field(min_length=3,max_length=150)
    description: str = Field(min_length=10)
    category: str
    location: str = Field(min_length=2,max_length=150)
    event_date: datetime
    ticket_price: float = Field(gt=0)
    banner_image: str | None = None
    total_tickets: int = Field(gt=0)

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
    created_at: datetime

    class Config:
        from_attributes = True