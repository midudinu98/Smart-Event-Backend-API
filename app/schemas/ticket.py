from pydantic import BaseModel
from datetime import datetime

class TicketResponse(BaseModel):
    id: int
    booking_id: int
    ticket_code: str
    qr_code_url: str
    created_at: datetime

    class Config:
        from_attributes = True