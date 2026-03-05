from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    phone_number: str
    password: str
    city: str
    state: str

class UserLogin(BaseModel):
    username_or_email_or_phone: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str
    city: str
    state: str

    class Config:
        from_attributes = True
