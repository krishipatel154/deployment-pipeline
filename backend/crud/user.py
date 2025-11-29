# crud/user.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate
from utils import hash_password
from utils.s3 import upload_to_s3
from fastapi import UploadFile


async def create_user(
    db: AsyncSession,
    user: UserCreate,
    profile_pic_file: UploadFile | None = None
):
    # Check if email exists
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar_one_or_none():
        return None

    hashed = hash_password(user.password)
    profile_pic_url = None

    if profile_pic_file:
        profile_pic_url = await upload_to_s3(profile_pic_file)

    db_user = User(
        email=user.email,
        hashed_password=hashed,
        profile_pic=profile_pic_url  # ← Save S3 URL
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()
