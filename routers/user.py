from fastapi import APIRouter, Depends,HTTPException,UploadFile, File

from app.models.user import User
from app.schemas.user import UserResponse,UserProfileUpdate
from app.utils.security import get_current_user

from sqlalchemy.orm import Session
from app.database import get_db

import os
import uuid
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.models.booking import Booking

router = APIRouter(prefix="/users",tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    
    return current_user

@router.put("/me")
def update_my_profile(profile: UserProfileUpdate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    if profile.username is None and profile.email is None:
        raise HTTPException(status_code=400,detail="Provide a username or email to update")

    if profile.username is not None:
        existing_user = db.query(User).filter(User.username == profile.username,User.id != current_user.id).first()

        if existing_user:
            raise HTTPException(status_code=400,detail="Username already exists")

        current_user.username = profile.username

    if profile.email is not None:
        existing_email = db.query(User).filter( User.email == profile.email,User.id != current_user.id).first()

        if existing_email:
            raise HTTPException(status_code=400,detail="Email already exists")

        current_user.email = profile.email

    db.commit()
    db.refresh(current_user)

    return {"message": "Profile updated successfully",
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email}

PROFILE_DIR = Path("static/profile_pictures")
PROFILE_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/me/profile-picture")
async def upload_profile_picture(file: UploadFile = File(...),
    db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    allowed_types = {"image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp"}

    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400,
            detail="Only JPEG, PNG, and WEBP images are allowed")

    content = await file.read()

    if not content:
        raise HTTPException(status_code=400,detail="Uploaded file is empty")

    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400,detail="Image must be smaller than 5 MB")

    filename = f"{uuid.uuid4().hex}{allowed_types[file.content_type]}"
    filepath = PROFILE_DIR / filename

    filepath.write_bytes(content)

    current_user.profile_picture = f"/static/profile_pictures/{filename}"

    db.commit()
    db.refresh(current_user)

    return {"message": "Profile picture uploaded successfully",
        "profile_picture": current_user.profile_picture}


@router.get("/me/booking-summary")
def get_booking_summary(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()

    total_bookings = len(bookings)

    confirmed_bookings = sum(1 for booking in bookings if booking.status == "CONFIRMED")

    pending_bookings = sum(1 for booking in bookings if booking.status == "PENDING")

    cancelled_bookings = sum(1 for booking in bookings if booking.status == "CANCELLED")

    total_tickets = sum(booking.ticket_quantity for booking in bookings)

    total_spent = sum(booking.total_price for booking in bookings if booking.status == "CONFIRMED")

    return {"user_id": current_user.id,
        "username": current_user.username,
        "total_bookings": total_bookings,
        "confirmed_bookings": confirmed_bookings,
        "pending_bookings": pending_bookings,
        "cancelled_bookings": cancelled_bookings,
        "total_tickets": total_tickets,
        "total_spent": total_spent}


