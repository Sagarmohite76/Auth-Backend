from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from db.session import engine
from models import Base
import db.base
from api.endpoints import users

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
