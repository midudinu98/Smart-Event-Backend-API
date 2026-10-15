
from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.events import Event
from app.models.event_view import EventView
from app.models.user import User
from app.models.booking import Booking
from app.models.events import EventStatus

from collections import Counter

from app.utils.security import get_current_user

router = APIRouter(prefix="/recommendations",tags=["Personalized Recommendations"])

@router.post("/view/{event_id}")
def track_event_view(event_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")

    view = EventView(user_id=current_user.id,event_id=event_id)

    db.add(view)
    db.commit()
    db.refresh(view)

    return {"message": "Event view tracked successfully",
        "event_id": event_id,
        "user_id": current_user.id}

@router.get("/my-preferences")
def get_my_preferences(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    bookings = (db.query(Event.category).join(Booking, Booking.event_id == Event.id)
        .filter(Booking.user_id == current_user.id).distinct().all())

    categories = [row[0] for row in bookings]

    return {"user_id": current_user.id,
        "booked_categories": categories}


@router.get("/for-me")
def get_personalized_recommendations(location: str | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    # 1. Get categories from previous bookings
    booked_rows = (db.query(Event.category).join(Booking, Booking.event_id == Event.id).filter(Booking.user_id == current_user.id,Booking.status != "CANCELLED").all())

    booked_categories = Counter(row[0] for row in booked_rows)

    # 2. Get categories from viewed events
    viewed_rows = (db.query(Event.category).join(EventView, EventView.event_id == Event.id).filter(EventView.user_id == current_user.id).all())

    viewed_categories = Counter(row[0] for row in viewed_rows)

    # 3. Count bookings for each event
    booking_rows = (db.query(Booking.event_id,db.query(Booking.id).filter(Booking.event_id == Booking.event_id).correlate(Booking).exists()))

    # Calculate popularity using booking counts
    from sqlalchemy import func

    popularity_rows = (db.query(Booking.event_id,func.count(Booking.id).label("booking_count"))
        .filter(Booking.status != "CANCELLED").group_by(Booking.event_id).all())

    popularity = {row.event_id: row.booking_count for row in popularity_rows}

    # 4. Get upcoming and ongoing events
    events = (db.query(Event).filter(Event.status.in_([EventStatus.UPCOMING,EventStatus.ONGOING])).all())

    # 5. Score each event
    recommendations = []

    for event in events:
        category_score = (booked_categories[event.category] * 3 + viewed_categories[event.category])

        location_score = 0

        if location and event.location:
            if location.strip().lower() in event.location.lower():
                location_score = 2

        popular_score = popularity.get(event.id, 0)

        total_score = (category_score+ location_score+ popular_score)

        recommendations.append({"event_id": event.id,
            "title": event.title,
            "category": event.category,
            "location": event.location,
            "event_date": event.event_date,
            "ticket_price": event.ticket_price,
            "booking_count": popular_score,
            "recommendation_score": total_score})

    # 6. Highest-scoring events first
    recommendations.sort(key=lambda item: (item["recommendation_score"],item["booking_count"]),reverse=True)

    return {"user_id": current_user.id,
        "preferred_categories": list(booked_categories.keys()),
        "location_filter": location,
        "recommendations": recommendations[:limit]}




