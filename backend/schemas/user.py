# schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    profile_pic: Optional[str] = None  # Will be filled with S3 URL after upload


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: Optional[datetime] = None
    is_active: bool = True
    is_superuser: bool = False
    profile_pic: Optional[str] = None   # ← NEW

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"