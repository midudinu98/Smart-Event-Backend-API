from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import NotificationResponse
from app.utils.security import get_current_user

from app.utils.notification import create_event_reminders


router = APIRouter(prefix="/notifications",tags=["Notifications"])

@router.get("/my-notifications",response_model=list[NotificationResponse])
def get_my_notifications(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    notifications = (db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc()).all())

    return notifications

@router.post("/create-event-reminders")
def create_reminders(db: Session = Depends(get_db)):
    create_event_reminders(db)
    return {"message": "Event reminders created successfully"}