from app.database import Base
from sqlalchemy import Column,Integer,String,DateTime
from datetime import datetime

from enum import Enum

class User(Base):

    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(50),nullable=False,unique=True,index=True)
    email=Column(String(100),nullable=False,unique=True,index=True)
    hashed_password=Column(String(255),nullable=False)
    role = Column(String(20), default="USER", nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)

class UserRole(str, Enum):
    USER = "USER"
    ORGANIZER = "ORGANIZER"
    ADMIN = "ADMIN"
   
