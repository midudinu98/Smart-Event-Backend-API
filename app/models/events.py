from app.database import Base
from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey
from datetime import datetime

from enum import Enum

from sqlalchemy import Enum as SQLEnum

class EventStatus(str, Enum):
    UPCOMING = "UPCOMING"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Event(Base):

    __tablename__="events"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(150),nullable=False,index=True)
    category = Column(String(50), nullable=False, index=True)
    location = Column(String(150), nullable=False)
    event_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    ticket_price = Column(Float, nullable=False)
    banner_image = Column(String(255), nullable=True)
    total_tickets = Column(Integer, nullable=False)
    available_tickets = Column(Integer, nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(SQLEnum(EventStatus),default=EventStatus.UPCOMING,nullable=False)    
    created_at = Column(DateTime,default=datetime.utcnow)




