from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import db.base
from api.endpoints import users
from core import Config

Base=declarative_base()


engine = create_engine(
    Config.DATABASE_URL,
    echo=False,           # set True only for local debugging
    pool_pre_ping=True,   # reconnect if an idle connection was dropped (critical on Render free tier)
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)



app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── DB ────────────────────────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── API routes ────────────────────────────────────────────────────────────
app.include_router(users.router)
print("🔥 APP STARTING...")