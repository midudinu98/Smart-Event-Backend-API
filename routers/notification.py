from fastapi import APIRouter, Depends,HTTPException
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

# Count unread notifications
@router.get("/unread-count")
def get_unread_count(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    count = (db.query(Notification).filter(Notification.user_id == current_user.id,Notification.is_read == False).count())

    return {"unread_count": count}

# Mark one notification as read
@router.patch("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    notification = (db.query(Notification).filter(Notification.id == notification_id,Notification.user_id == current_user.id).first())

    if notification is None:
        raise HTTPException(status_code=404,detail="Notification not found")

    notification.is_read = True
    db.commit()
    db.refresh(notification)

    return {"message": "Notification marked as read",
        "is_read": notification.is_read}


# Mark all notifications as read
@router.patch("/read-all")
def mark_all_notifications_read(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    count = (db.query(Notification).filter(Notification.user_id == current_user.id,Notification.is_read == False)
        .update({Notification.is_read: True},synchronize_session=False))

    db.commit()

    return {"message": "All notifications marked as read",
        "updated_count": count}

@router.patch("/{notification_id}/read")
def mark_notification_as_read(notification_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    notification = db.query(Notification).filter(Notification.id == notification_id,
        Notification.user_id == current_user.id).first()

    if not notification:
        raise HTTPException(status_code=404,detail="Notification not found")

    notification.is_read = True
    db.commit()

    return {"message": "Notification marked as read"}


@router.patch("/read-all")
def mark_all_notifications_as_read(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    db.query(Notification).filter(Notification.user_id == current_user.id,
        Notification.is_read == False).update({Notification.is_read: True},synchronize_session=False)

    db.commit()

    return {"message": "All notifications marked as read"}
