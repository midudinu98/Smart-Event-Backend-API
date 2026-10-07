from app.database import Base
from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey
from datetime import datetime


class Booking(Base):
    
    __tablename__ = "booking"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    ticket_quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    booking_status = Column(String, default="PENDING", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)