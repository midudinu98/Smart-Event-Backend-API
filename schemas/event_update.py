from pydantic import BaseModel, ConfigDict
from datetime import datetime

class EventUpdateCreate(BaseModel):
    event_id: int
    message: str

class EventUpdateResponse(BaseModel):
    id: int
    event_id: int
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
