from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User,UserRole
from app.schemas.user import Token, UserCreate,UserLogin, UserResponse
from app.utils.security import create_access_token,hash_password,verify_password


router = APIRouter(prefix="/auth",tags=["Authentication"])


@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(user_data: UserLogin,db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")

    existing_username = db.query(User).filter(User.username == user_data.username).first()

    if existing_username:
        raise HTTPException(status_code=400,detail="Username already exists")

    hashed_password = hash_password(user_data.password)

    new_user = User(username=user_data.username,email=user_data.email,hashed_password=hashed_password,role=UserRole.USER)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login(user_data: UserLogin,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user:
        raise HTTPException(status_code=401,detail="Invalid email or password")

    if not verify_password(user_data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid email or password")

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})

    return {"access_token": access_token,"token_type": "bearer"}