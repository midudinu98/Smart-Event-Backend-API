from pydantic import BaseModel,EmailStr,Field
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email:EmailStr
    password: str = Field(min_length=1, max_length=128)
    
class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr
    role:str
    created_at:datetime
    

class Config:
    from_attribute=True

class Token(BaseModel):
    access_token:str
    token_type:str   

class AdminUserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True         

