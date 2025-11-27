from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate
from utils import hash_password


async def create_user(db: AsyncSession, user: UserCreate):
    # Check if user already exists
    query = select(User).where(User.email == user.email)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        return None  # User exists

    hashed = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()
