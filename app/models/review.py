from app.database import Base
from sqlalchemy import Column,Integer,Text,DateTime,ForeignKey,UniqueConstraint
from datetime import datetime

class Review(Base):
    
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False,index=True,)
    event_id = Column(Integer,ForeignKey("events.id"),nullable=False,index=True,)
    rating = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=True)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "event_id",
            name="unique_user_event_review"),)
