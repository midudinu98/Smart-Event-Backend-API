from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from datetime import datetime, timezone

from app.database import get_db
from app.models.coupon import Coupon
from app.schemas.coupon import CouponCreate,CouponResponse,CouponApply


router = APIRouter(prefix="/coupons",tags=["Coupons"])

# Create a coupon
@router.post("", response_model=CouponResponse)
def create_coupon(coupon_data: CouponCreate,db: Session = Depends(get_db)):
    existing_coupon = db.query(Coupon).filter(Coupon.coupon_code == coupon_data.coupon_code).first()

    if existing_coupon:
        raise HTTPException(status_code=400,detail="Coupon code already exists")

    new_coupon = Coupon(**coupon_data.model_dump())

    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)

    return new_coupon


# Get all coupons
@router.get("", response_model=list[CouponResponse])
def get_coupons(db: Session = Depends(get_db)):
    return db.query(Coupon).all()


# Validate a coupon
@router.post("/validate")
def validate_coupon(coupon_data: CouponApply,db: Session = Depends(get_db)):
    coupon = db.query(Coupon).filter(Coupon.coupon_code == coupon_data.coupon_code).first()

    if not coupon:
        raise HTTPException(status_code=404,detail="Coupon not found")

    if not coupon.is_active:
        raise HTTPException(status_code=400,detail="Coupon is inactive")

    now = datetime.now(timezone.utc)

    expiry = coupon.expiry_date
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)

    if expiry <= now:
        raise HTTPException(status_code=400,detail="Coupon has expired")

    if coupon.used_count >= coupon.usage_limit:
        raise HTTPException(status_code=400,detail="Coupon usage limit reached")

    if coupon_data.booking_amount < coupon.minimum_booking_amount:
        raise HTTPException( status_code=400,detail="Booking amount is below the minimum required")

    if coupon.discount_type.value == "PERCENTAGE":
        discount = (coupon_data.booking_amount* coupon.discount_value/ 100)
    else:
        discount = coupon.discount_value

    # Discount cannot exceed the booking amount
    discount = min(discount, coupon_data.booking_amount)

    final_amount = coupon_data.booking_amount - discount

    return {"message": "Coupon applied successfully",
        "coupon_code": coupon.coupon_code,
        "booking_amount": round(coupon_data.booking_amount, 2),
        "discount_amount": round(discount, 2),
        "final_amount": round(final_amount, 2)}
