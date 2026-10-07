from app.database import Base
from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey
from datetime import datetime

class Ticket(Base):
    
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer,ForeignKey("booking.id"),nullable=False)
    ticket_code = Column(String,unique=True,nullable=False,index=True)
    qr_code_url = Column(String,nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)