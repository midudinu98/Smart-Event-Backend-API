from pydantic import BaseModel
from datetime import datetime

from app.models.notification import NotificationType

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: str
    notification_type: NotificationType
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationReadUpdate(BaseModel):
    is_read: bool
