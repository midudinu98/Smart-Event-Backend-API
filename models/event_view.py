from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime

from app.database import Base

class EventView(Base):
    
    __tablename__ = "event_views"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False,index=True)
    event_id = Column(Integer,ForeignKey("events.id"),nullable=False,index=True)
    viewed_at = Column(DateTime,default=datetime.utcnow,nullable=False)
