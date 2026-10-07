from app.database import Base
from sqlalchemy import Column,Integer,String,Float,DateTime
from datetime import datetime

class Event(Base):

    __tablename__="events"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(150),nullable=False,index=True)
    category = Column(String(50), nullable=False, index=True)
    location = Column(String(150), nullable=False)
    event_date = Column(DateTime, nullable=False)
    ticket_price = Column(Float, nullable=False)
    banner_image = Column(String(255), nullable=True)
    total_tickets = Column(Integer, nullable=False)
    available_tickets = Column(Integer, nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)