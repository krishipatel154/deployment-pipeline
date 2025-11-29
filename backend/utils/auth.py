# utils.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
import jwt
from dotenv import load_dotenv
load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


secret = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")

if secret is None or algorithm is None:
    raise ValueError("SECRET_KEY and ALGORITHM must be set")

SECRET_KEY: str = secret
ALGORITHM: str = algorithm
ACCESS_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    to_encode["exp"] = expire

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
