from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base


class EventUpdate(Base):
    
    __tablename__ = "event_updates"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer,ForeignKey("events.id"),nullable=False,index=True)
    message = Column(String, nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
