# # database.py
# import os
# from dotenv import load_dotenv
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from models.user import Base

# load_dotenv()

# # change database url
# db_url = os.getenv("DATABASE_URL")
# if db_url is None:
#     raise ValueError("DATABASE_URL is missing in environment")

# DATABASE_URL: str = db_url

# engine = create_async_engine(DATABASE_URL, echo=True)

# AsyncSessionLocal = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )


# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session


# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# database.py
import os
import ssl
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.user import Base  # Make sure this imports your SQLAlchemy models

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing in environment")

# SSL support for AWS RDS
connect_args = {}
if "rds.amazonaws.com" in DATABASE_URL:
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    connect_args = {"ssl": ssl_context}

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args=connect_args
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Dependency to use in FastAPI routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# Function to create tables on startup
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
