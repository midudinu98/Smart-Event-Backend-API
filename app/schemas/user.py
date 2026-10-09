from pydantic import BaseModel,EmailStr,Field
from datetime import datetime

class UserCreate(BaseModel):
    username:str= Field(min_length=3,max_length=50)
    password:str= Field(max_length=6,min_length=100)


class UserLogin(BaseModel):
    email:EmailStr
    password:str

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
    token_types:str   

class AdminUserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True         

