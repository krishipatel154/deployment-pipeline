# main.py
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    File,
    UploadFile,
    Form,
    Request,
    Response,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, create_tables
from schemas.user import UserCreate, UserOut
from crud.user import create_user  # ← now accepts profile_pic_file
from contextlib import asynccontextmanager
from schemas.user import LoginRequest, TokenResponse
from crud.user import get_user_by_email
from utils.auth import verify_password, create_access_token
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from metrics import REQUEST_COUNT, REQUEST_LATENCY
import time


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="Website Builder AI",
    version="0.1.0",
    lifespan=lifespan
)


# CORS — add your production domain later
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://13.202.225.101:5173",
        "http://13.202.225.101:8000",
        "http://13.202.225.101"
        # Add your real domain later, e.g.:
        # "https://yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        http_status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        endpoint=request.url.path
    ).observe(latency)

    return response


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# ──────────────────────────────────────────────────────────────
# SIGNUP WITH OPTIONAL PROFILE PICTURE (S3)
# ──────────────────────────────────────────────────────────────
@app.post(
    "/signup",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
async def signup(
    email: str = Form(...),
    password: str = Form(...),
    profile_pic: UploadFile = File(None),   # ← Optional file upload
    db: AsyncSession = Depends(get_db)
):

    user_in = UserCreate(email=email, password=password)

    db_user = await create_user(db, user_in, profile_pic_file=profile_pic)
    if not db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return db_user


# ──────────────────────────────────────────────────────────────
# LOGIN (unchanged)
# ──────────────────────────────────────────────────────────────
@app.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, data.email)

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)


@app.get("/")
async def root():
    return {"message": "Website Builder AI - Now with S3 + RDS!"}
