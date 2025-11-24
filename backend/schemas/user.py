from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import os

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: Optional[datetime] = None  # ← changed to datetime
    is_active: bool = True
    is_superuser: bool = False

    class Config:
        from_attributes = True  # this allows ORM mode (SQLAlchemy → Pydantic)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"