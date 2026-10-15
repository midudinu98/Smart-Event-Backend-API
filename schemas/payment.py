from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PaymentCreate(BaseModel):
    booking_id: int
    payment_method: str

class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    payment_method: str
    payment_status: str
    transaction_id: Optional[str] = None
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True
