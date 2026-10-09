from pydantic import BaseModel, Field
from datetime import datetime

class BookingCreate(BaseModel):
    event_id: int
    ticket_quantity: int = Field(gt=0)

class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    ticket_quantity: int
    total_price: float
    booking_status: str
    created_at: datetime

    class Config:
        from_attributes = True