
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base

class Payment(Base):
    
    __tablename__ = "payments"

    id=Column(Integer, primary_key=True, index=True)
    booking_id=Column(Integer,ForeignKey("booking.id"),nullable=False,index=True)
    payment_method=Column(String(50), nullable=False)
    payment_status=Column(String(20),default="PENDING",nullable=False)
    transaction_id=Column(String(100), unique=True, nullable=True)
    amount=Column(Float, nullable=False)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)               
