from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.user import UserResponse
from app.utils.security import get_current_user


router = APIRouter(prefix="/users",tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user