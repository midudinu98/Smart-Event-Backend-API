from app.database import Base
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,Boolean,Enum
from datetime import datetime

from sqlalchemy.sql import func
import enum

class NotificationType(str, enum.Enum):
    EVENT = "EVENT"
    BOOKING = "BOOKING"
    PAYMENT = "PAYMENT"
    SYSTEM = "SYSTEM"

class Notification(Base):
    
    __tablename__ = "notifications"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    event_id = Column(Integer,ForeignKey("events.id"),nullable=False)
    title = Column(String,nullable=False)
    message = Column(String,nullable=False)
    notification_type = Column(Enum(NotificationType),nullable=False,default=NotificationType.SYSTEM)
    is_read = Column(Boolean,default=False,nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)