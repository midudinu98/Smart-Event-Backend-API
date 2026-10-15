
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.review import Review
from app.models.user import User
from app.models.events import Event
from app.models.booking import Booking
from app.schemas.review import ReviewCreate,ReviewUpdate,ReviewResponse

from app.utils.security import get_current_user

from sqlalchemy import func

router = APIRouter(prefix="/reviews",tags=["Reviews"],)

@router.post("/",response_model=ReviewResponse,status_code=status.HTTP_201_CREATED)
def create_review(review_data: ReviewCreate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    # Check whether the event exists
    event = db.query(Event).filter(Event.id == review_data.event_id).first()

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Event not found")

    # Check whether the event has been completed
    if event.event_status != "COMPLETED":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You can review only completed events")

    # Check whether the user has a confirmed booking
    booking = db.query(Booking).filter(Booking.user_id == current_user.id,
        Booking.event_id == review_data.event_id,
        Booking.booking_status == "CONFIRMED").first()

    if not booking:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You must have a confirmed booking to review this event")

    # Prevent duplicate reviews
    existing_review = db.query(Review).filter(Review.user_id == current_user.id,Review.event_id == review_data.event_id).first()

    if existing_review:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You have already reviewed this event")

    # Create the review
    new_review = Review(user_id=current_user.id,
        event_id=review_data.event_id,
        rating=review_data.rating,
        review_text=review_data.review_text)

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review


@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int,review_data: ReviewUpdate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Review not found")

    # Only the review owner can update it
    if review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You can update only your own reviews")

    # Update only fields supplied in the request
    update_data = review_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Provide at least one field to update")

    for field, value in update_data.items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)

    return review

@router.delete("/{review_id}")
def delete_review(review_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Review not found")

    # Only the review owner can delete it
    if review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You can delete only your own reviews")

    db.delete(review)
    db.commit()

    return {"message": "Review deleted successfully"}


@router.get("/event/{event_id}")
def get_event_reviews(
    event_id: int,
    db: Session = Depends(get_db),
):
    # Check whether the event exists
    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    # Fetch reviews for this event
    reviews = db.query(Review).filter(
        Review.event_id == event_id
    ).order_by(Review.created_at.desc()).all()

    # Calculate average rating
    average_rating = db.query(
        func.avg(Review.rating)
    ).filter(
        Review.event_id == event_id
    ).scalar()

    return {
        "event_id": event_id,
        "total_reviews": len(reviews),
        "average_rating": round(average_rating, 2)
        if average_rating is not None else 0,
        "reviews": reviews,
    }

@router.get("/event/{event_id}/rating")
def get_event_average_rating(event_id: int,db: Session = Depends(get_db)):
    # Check whether the event exists
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Event not found")

    average_rating = db.query(func.avg(Review.rating)).filter(Review.event_id == event_id).scalar()

    total_reviews = db.query(Review).filter(Review.event_id == event_id).count()

    return {"event_id": event_id,
        "total_reviews": total_reviews,
        "average_rating": round(average_rating, 2)
        if average_rating is not None else 0}




