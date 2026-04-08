# =========================
# Imports
# =========================
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import (
    Column, Integer, String, DateTime, Enum, Float,
    Boolean, ForeignKey, TIMESTAMP, create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from sqlalchemy.sql import func
from datetime import datetime
import enum
import hashlib
import random

# =========================
# Config
# =========================
class Config:
    DATABASE_URL = "sqlite:///./test.db"  # Replace with your DB

# =========================
# Base
# =========================
Base = declarative_base()

# =========================
# Enums
# =========================
class RoleEnum(enum.Enum):
    admin = "admin"
    user = "user"

# =========================
# Models
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum, name="user_role"), default=RoleEnum.user, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    students = relationship("Student", back_populates="user", cascade="all, delete")

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    full_name = Column(String(100), nullable=False)
    age = Column(Integer)
    class_name = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="students")
    predictions = relationship("Prediction", back_populates="student", cascade="all, delete")
    performances = relationship("Performance", back_populates="student", cascade="all, delete")

class Performance(Base):
    __tablename__ = 'performance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    study_hours = Column(Float)
    attendance = Column(Float)
    previous_score = Column(Float)
    assignments_completed = Column(Integer)
    extracurricular = Column(Boolean)
    created_at = Column(TIMESTAMP, server_default=func.now())

    student = relationship("Student", back_populates="performances")
    predictions = relationship("Prediction", back_populates="performance", cascade="all, delete")

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    performance_id = Column(Integer, ForeignKey('performance.id', ondelete='CASCADE'), nullable=False)
    predicted_label = Column(Enum('Pass', 'Fail', name='prediction_label_enum'), nullable=False)
    probability_score = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())

    student = relationship("Student", back_populates="predictions")
    performance = relationship("Performance", back_populates="predictions")

# =========================
# Database
# =========================
engine = create_engine(
    Config.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base.metadata.create_all(bind=engine)

# =========================
# FastAPI App
# =========================
app = FastAPI()
origins = ["http://localhost:8000", "http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# Utility Functions
# =========================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

otp_store = {}  # Temporary in-memory storage for OTPs

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def save_otp(email: str, otp: str):
    otp_store[email] = otp

def verify_otp(email: str, otp: str):
    if otp_store.get(email) == otp:
        del otp_store[email]
        return "OTP verified successfully"
    return "Invalid or expired OTP"

def send_email(email: str, otp: str):
    print(f"[EMAIL] Sent OTP {otp} to {email}")  # Placeholder for real email service

# =========================
# CRUD Functions
# =========================
def create_user(db: Session, name: str, email: str, password: str):
    user = User(name=name, email=email, password=password, role=RoleEnum.user)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def update_password(email: str, new_password_hash: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    user.password = new_password_hash
    db.commit()
    db.refresh(user)
    return user

# =========================
# Schemas (Pydantic)
# =========================
from pydantic import BaseModel

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class EmailRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str

class VerifyOTPRequest(BaseModel):
    email: str
    otp: str

# =========================
# Router for Auth
# =========================
router = APIRouter()

@router.post("/register")
def add_user(user: UserRegister, db: Session = Depends(get_db)):
    if get_user_by_email(user.email, db):
        raise HTTPException(status_code=400, detail="Email already registered")
    create_user(db, user.name, user.email, hash_password(user.password))
    return {"message": "User registered successfully."}

@router.get("/users")
def getUsers(db: Session = Depends(get_db)):
    return get_users(db)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(user.email, db)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if verify_password(user.password, db_user.password):
        return {"message": "Login successful", "user": {"name": db_user.name, "email": db_user.email, "role": db_user.role.value}}
    raise HTTPException(status_code=401, detail="Invalid password")

@router.post("/send-otp")
def send_otp_route(request: EmailRequest, db: Session = Depends(get_db)):
    db_user = get_user_by_email(request.email, db)
    if not db_user:
        raise HTTPException(status_code=404, detail="Enter registered email address")
    otp = generate_otp()
    save_otp(request.email, otp)
    send_email(request.email, otp)
    return {"message": "OTP sent successfully"}

@router.post("/verify-otp")
def verify_otp_route(request: VerifyOTPRequest):
    result = verify_otp(request.email, request.otp)
    if result == "OTP verified successfully":
        return {"message": result}
    raise HTTPException(status_code=400, detail=result)

@router.post("/reset-password")
def reset_password_route(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    db_user = get_user_by_email(request.email, db)
    if not db_user:
        raise HTTPException(status_code=404, detail="Enter registered email address")
    hashed = hash_password(request.new_password)
    update_password(db_user.email, hashed, db)
    return {"message": "Password reset successfully"}

# =========================
# Include router in app
# =========================
app.include_router(router)

print("🔥 APP STARTING...")