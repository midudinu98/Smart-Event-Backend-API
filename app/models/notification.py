from app.database import Base
from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey,Boolean
from datetime import datetime

class Notification(Base):
    
    __tablename__ = "notifications"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    event_id = Column(Integer,ForeignKey("events.id"),nullable=False)
    title = Column(String,nullable=False)
    message = Column(String,nullable=False)
    type = Column(String,nullable=False)
    is_read = Column(Boolean,default=False,nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)