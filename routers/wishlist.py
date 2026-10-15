from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.events import Event
from app.models.wishlist import Wishlist
from app.schemas.wishlist import WishlistCreate, WishlistResponse
from app.utils.security import get_current_user

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])

@router.post("/", response_model=WishlistResponse,status_code=status.HTTP_201_CREATED)
def add_to_wishlist(data: WishlistCreate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    event = db.query(Event).filter(Event.id == data.event_id).first()

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")

    existing = db.query(Wishlist).filter(Wishlist.user_id == current_user.id,Wishlist.event_id == data.event_id).first()

    if existing:
        raise HTTPException(status_code=400,detail="Event already exists in wishlist")

    wishlist_item = Wishlist(user_id=current_user.id,event_id=data.event_id)

    db.add(wishlist_item)
    db.commit()
    db.refresh(wishlist_item)

    return wishlist_item

@router.get("/", response_model=list[WishlistResponse])
def get_my_wishlist(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    return db.query(Wishlist).filter(Wishlist.user_id == current_user.id).order_by(Wishlist.created_at.desc()).all()

@router.delete("/{event_id}")
def remove_from_wishlist(event_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    wishlist_item = db.query(Wishlist).filter(Wishlist.user_id == current_user.id,Wishlist.event_id == event_id).first()

    if not wishlist_item:
        raise HTTPException(status_code=404,detail="Event not found in your wishlist")

    db.delete(wishlist_item)
    db.commit()

    return {"message": "Event removed from wishlist successfully"}
