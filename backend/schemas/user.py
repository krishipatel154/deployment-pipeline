from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

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