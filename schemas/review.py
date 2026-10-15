from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ReviewCreate(BaseModel):
    event_id: int
    rating: int = Field(..., ge=1, le=5)
    review_text: str | None = None

class ReviewUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    review_text: str | None = None

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    rating: int
    review_text: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
