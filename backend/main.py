from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, create_tables
from schemas.user import UserCreate, UserOut
from crud.user import create_user
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    await create_tables()
    yield
    # Shutdown: cleanup if needed

app = FastAPI(
    title="Website Builder AI", 
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await create_user(db, user)
    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return db_user

@app.get("/")
async def root():
    return {"message": "Website Builder AI - Signup is ready!"}