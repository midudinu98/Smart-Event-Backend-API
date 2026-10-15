from app.database import Base
from sqlalchemy import Column,Integer,String,Float,DateTime,Boolean,Enum
from datetime import datetime

class DiscountType(str, __import__("enum").Enum):
    PERCENTAGE = "PERCENTAGE"
    FIXED = "FIXED"

class Coupon(Base):
    
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    coupon_code = Column(String(50),unique=True,nullable=False,index=True,)
    discount_type = Column( Enum(DiscountType),nullable=False,)
    discount_value = Column(Float, nullable=False)
    minimum_booking_amount = Column(Float,default=0.0,nullable=False,)
    expiry_date = Column(DateTime, nullable=False)
    usage_limit = Column(Integer, nullable=False)
    used_count = Column(Integer,default=0,nullable=False,)
    is_active = Column(Boolean,default=True,nullable=False,)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False,)
