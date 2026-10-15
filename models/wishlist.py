from app.database import Base
from sqlalchemy import Column,Integer,DateTime,ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

class Wishlist(Base):
    
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False,index=True)
    event_id = Column(Integer,ForeignKey("events.id"),nullable=False,index=True)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)

    event = relationship("Event")
    user = relationship("User")

